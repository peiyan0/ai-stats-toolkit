import os
import re
import math
import requests

class RAGEngine:
    def __init__(self, kb_dir=None, model="phi3.5:3.8b"):
        self.model = model
        self.base_url = "http://127.0.0.1:11434/api"
        if kb_dir is None:
            kb_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")
        self.kb_dir = kb_dir
        self.chunks = []
        self.tfidf_index = None
        self._load_and_chunk_docs()

    def _load_and_chunk_docs(self):
        """Loads and chunks knowledge base markdown files."""
        if not os.path.exists(self.kb_dir):
            return
            
        for filename in os.listdir(self.kb_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(self.kb_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Split chunks by headers (e.g., ## or ###) or large blank lines
                sections = re.split(r'\n(?=##+ )', content)
                for sec in sections:
                    clean_sec = sec.strip()
                    if clean_sec:
                        self.chunks.append(clean_sec)
                        
        if self.chunks:
            self.tfidf_index = SimpleTFIDFIndex(self.chunks)

    def _get_ollama_embedding(self, text):
        """Fetches embedding from local Ollama service with multi-endpoint fallback."""
        # Try nomic-embed-text first, fallback to the main causal model (phi3.5)
        for emb_model in ["nomic-embed-text", "all-minilm", self.model]:
            # Try /api/embed endpoint (standard in newer Ollama)
            try:
                res = requests.post(f"{self.base_url}/embed", json={
                    "model": emb_model,
                    "input": text
                }, timeout=3)
                if res.status_code == 200:
                    data = res.json()
                    if "embeddings" in data and len(data["embeddings"]) > 0:
                        return data["embeddings"][0]
            except Exception:
                pass
                
            # Fallback to /api/embeddings (classic endpoint)
            try:
                res = requests.post(f"{self.base_url}/embeddings", json={
                    "model": emb_model,
                    "prompt": text
                }, timeout=3)
                if res.status_code == 200:
                    return res.json().get("embedding")
            except Exception:
                pass
        return None

    def _cosine_similarity(self, v1, v2):
        """Calculates cosine similarity between two float vectors."""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = sum(a * a for a in v1) ** 0.5
        magnitude2 = sum(b * b for b in v2) ** 0.5
        if magnitude1 * magnitude2 == 0:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    def retrieve_relevant_context(self, query, top_k=2):
        """
        Retrieves top-k context chunks relevant to the query.
        Uses Ollama embeddings if available, otherwise falls back to robust pure-Python TF-IDF.
        """
        if not self.chunks:
            return ""

        # Step 1: Attempt semantic search via Ollama
        query_embedding = self._get_ollama_embedding(query)
        if query_embedding:
            scores = []
            for chunk in self.chunks:
                chunk_emb = self._get_ollama_embedding(chunk[:500]) # embed starting section of chunk for speed
                if chunk_emb:
                    sim = self._cosine_similarity(query_embedding, chunk_emb)
                    scores.append((sim, chunk))
            
            if scores:
                scores.sort(key=lambda x: x[0], reverse=True)
                return "\n\n---\n\n".join([chunk for sim, chunk in scores[:top_k]])

        # Step 2: Fallback to high-fidelity TF-IDF index
        if self.tfidf_index:
            relevant_chunks = self.tfidf_index.search(query, top_k=top_k)
            return "\n\n---\n\n".join(relevant_chunks)
            
        return ""


class SimpleTFIDFIndex:
    """A high-performance, zero-dependency pure-Python TF-IDF search engine."""
    def __init__(self, chunks):
        self.chunks = chunks
        self.doc_term_freqs = []
        self.df = {}
        self.num_docs = len(chunks)
        self.vocab = set()
        self._build_index()

    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def _build_index(self):
        for chunk in self.chunks:
            tokens = self._tokenize(chunk)
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            self.doc_term_freqs.append(tf)
            self.vocab.update(tf.keys())
            
            for t in tf.keys():
                self.df[t] = self.df.get(t, 0) + 1

    def _get_tfidf_vector(self, tokens):
        vector = {}
        for t in tokens:
            if t in self.vocab:
                tf = tokens.count(t)
                idf = math.log((self.num_docs + 1) / (self.df.get(t, 0) + 1)) + 1
                vector[t] = tf * idf
        return vector

    def search(self, query, top_k=2):
        query_tokens = self._tokenize(query)
        query_vector = self._get_tfidf_vector(query_tokens)
        
        if not query_vector:
            return self.chunks[:top_k]
            
        scores = []
        for i, doc_tf in enumerate(self.doc_term_freqs):
            dot_product = 0.0
            query_magnitude_sq = 0.0
            doc_magnitude_sq = 0.0
            
            doc_vector = {}
            for t, tf_val in doc_tf.items():
                idf = math.log((self.num_docs + 1) / (self.df.get(t, 0) + 1)) + 1
                doc_vector[t] = tf_val * idf
                
            all_terms = set(query_vector.keys()).union(set(doc_vector.keys()))
            for t in all_terms:
                q_val = query_vector.get(t, 0.0)
                d_val = doc_vector.get(t, 0.0)
                dot_product += q_val * d_val
                query_magnitude_sq += q_val ** 2
                doc_magnitude_sq += d_val ** 2
                
            mag_query = query_magnitude_sq ** 0.5
            mag_doc = doc_magnitude_sq ** 0.5
            
            similarity = 0.0
            if mag_query * mag_doc > 0:
                similarity = dot_product / (mag_query * mag_doc)
            
            scores.append((similarity, self.chunks[i]))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scores[:top_k]]
