import requests
import json
from stats_logic.rag_engine import RAGEngine

class AIConsultant:
    def __init__(self, model="phi3.5:3.8b"):
        self.model = model
        self.base_url = "http://127.0.0.1:11434/api"
        self.generate_url = f"{self.base_url}/generate"
        self.tags_url = f"{self.base_url}/tags"
        # Initialize high-craft RAG engine
        self.rag = RAGEngine(model=model)

    def is_available(self):
        """Checks if Ollama is running and the model is pulled."""
        try:
            response = requests.get(self.tags_url, timeout=5)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                return self.model in models or f"{self.model}:latest" in models
            return False
        except:
            return False

    def interpret_results(self, test_name, data_summary, results):
        """
        Interprets statistical results using local Ollama, augmented with RAG context.
        """
        # Retrieve context from local APA 7th standards
        rag_context = self.rag.retrieve_relevant_context(
            f"How to report {test_name} result in APA 7th style with metrics {json.dumps(results)}"
        )
        
        prompt = f"""<|system|>
You are a Senior Statistical Consultant. Interpret the results below concisely. Provide exactly 3 bullet points. 
Do not repeat context, system instructions, or notes.
Ground your interpretation in these verified standards if applicable:
{rag_context}

<|user|>
CONTEXT:
- Test: {test_name}
- Sample Size/Context: {data_summary}
- Metrics: {json.dumps(results, indent=2)}

ANALYSIS GUIDELINES:
1. P-value vs alpha=0.05.
2. Effect size/Magnitude.
3. 1 Practical takeaway.

<|assistant|>
"""
        
        try:
            response = requests.post(self.generate_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "stop": ["<|system|>", "<|user|>", "[SYSTEM:"],
                    "num_predict": 256
                }
            }, timeout=90)
            
            if response.status_code == 200:
                raw_text = response.json().get('response', "").strip()
                if "[SYSTEM:" in raw_text:
                    raw_text = raw_text.split("[SYSTEM:")[0].strip()
                return raw_text if raw_text else self.rule_based_fallback(test_name, results)
            else:
                return self.rule_based_fallback(test_name, results)
        except Exception as e:
            return self.rule_based_fallback(test_name, results)

    def rule_based_fallback(self, test_name, results):
        """
        Fallback logic if Ollama is unavailable.
        """
        # Basic logic for p-values
        p_value = results.get('p_value') or results.get('p')
        if p_value is not None:
            sig = "statistically significant" if p_value < 0.05 else "not statistically significant"
            return f"The {test_name} result is {sig} (p={p_value:.4f}). This suggests that the observed patterns are {'likely' if p_value < 0.05 else 'unlikely'} to be due to chance."
        
        return "Calculation complete. Please review the raw values above for your analysis."

    def get_test_recommendation(self, user_goal, data_type, group_count):
        """
        Uses AI to recommend a statistical test based on user input, augmented with RAG decision tree context.
        Optimized for Phi-3.5 with strict formatting to prevent instruction leakage.
        """
        # Retrieve decision criteria context from local matrix
        rag_context = self.rag.retrieve_relevant_context(
            f"Select test for objective: {user_goal} with data type: {data_type} and {group_count} groups"
        )
        
        prompt = f"""<|system|>
You are a Senior Statistical Methodologist. Provide a precise, single-test recommendation based on the user's research design.
Do not repeat these instructions in your response.
Ground your decision in this decision matrix reference:
{rag_context}

<|user|>
RESEARCH DESIGN:
- Objective: {user_goal}
- Data Type: {data_type}
- Number of Groups: {group_count}

INSTRUCTIONS:
1. Identify the core statistical need (Comparison, Relationship, or Prediction).
2. Select the most appropriate test.
3. Provide the output in the format:
**Test Name**
[2-sentence justification]

<|assistant|>
"""
        
        try:
            response = requests.post(self.generate_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1, # High precision
                    "stop": ["<|system|>", "<|user|>", "[SYSTEM:"], # Prevent leakage
                    "num_predict": 150
                }
            }, timeout=90)
            if response.status_code == 200:
                raw_text = response.json().get('response', "").strip()
                # Sanity check: remove any leaked prompt fragments if they appear
                if "[SYSTEM:" in raw_text:
                    raw_text = raw_text.split("[SYSTEM:")[0].strip()
                return raw_text if raw_text else "Based on your input, please consult a statistical chart."
            else:
                return "AI consultant is currently offline. Please consult standard testing guidelines."
        except Exception as e:
            return "Unable to provide an AI recommendation at this time."
