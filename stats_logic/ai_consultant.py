import json
import requests
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded immediately on import
load_dotenv()

class AIConsultant:
    def __init__(self):
        # Load cloud configurations from environment if available
        self.cloud_model = os.getenv("OLLAMA_MODEL")
        self.cloud_base_url = os.getenv("OLLAMA_BASE_URL")
        self.cloud_api_key = os.getenv("OLLAMA_API_KEY")

        # Local connection configurations
        self.local_url = "http://127.0.0.1:11434/api"
        self.model = self.cloud_model if self.cloud_model else "phi3.5:3.8b"
        self.headers = {"Content-Type": "application/json"}
        self._connected = None

    def check_ollama_status(self):
        """
        Dynamically checks if local/cloud Ollama is active and selects the model.
        Returns (is_available, model_name).
        """
        if self.cloud_base_url:
            return True, self.model

        try:
            response = requests.get(f"{self.local_url}/tags", timeout=1.5)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                # Look for our priority models
                for candidate in ["phi3.5:3.8b", "llama3.1:latest", "phi3.5", "llama3.1"]:
                    if candidate in models or f"{candidate}:latest" in models:
                        self.model = candidate
                        return True, candidate
                if len(models) > 0:
                    self.model = models[0]
                    return True, models[0]
            return False, None
        except Exception:
            return False, None

    def _call_local_llm(self, prompt, temperature=0.2, max_tokens=400):
        """
        Performs high-reliability connection to local or cloud Ollama instance.
        """
        if self.cloud_base_url:
            try:
                headers = {"Content-Type": "application/json"}
                if self.cloud_api_key:
                    headers["Authorization"] = f"Bearer {self.cloud_api_key}"

                # 1. If it's a v1 endpoint, use OpenAI-compatible format
                if "/v1" in self.cloud_base_url:
                    url = f"{self.cloud_base_url.rstrip('/')}/chat/completions"
                    payload = {
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                    response = requests.post(url, json=payload, headers=headers, timeout=45)
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content'].strip()

                # 2. Otherwise/Fallback, use native Ollama /generate format
                if "/v1" in self.cloud_base_url:
                    # Deriving the native /generate URL by replacing /v1 with /api
                    url = f"{self.cloud_base_url.rstrip('/').replace('/v1', '')}/api/generate"
                else:
                    url = f"{self.cloud_base_url.rstrip('/')}/generate"
                    
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "stop": ["<|system|>", "<|user|>", "[SYSTEM:"]
                    }
                }
                response = requests.post(url, json=payload, headers=headers, timeout=45)
                if response.status_code == 200:
                    return response.json().get('response', "").strip()
            except Exception as e:
                # Log error and fall through to local fallback
                print(f"Cloud LLM call failed, falling back to local: {e}")
                pass

        # Local Ollama Fallback
        is_active, active_model = self.check_ollama_status()
        if not is_active:
            return None

        try:
            response = requests.post(
                f"{self.local_url}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "stop": ["<|system|>", "<|user|>", "[SYSTEM:"]
                    }
                },
                headers={"Content-Type": "application/json"},
                timeout=45
            )
            if response.status_code == 200:
                return response.json().get('response', "").strip()
        except Exception:
            pass
        return None

    def interpret_results(self, test_name, data_summary, results):
        """
        Interprets statistical results instantly using high-performance, 
        deterministic mathematical and statistical guidelines.
        """
        return self.rule_based_interpretation(test_name, results)

    def rule_based_interpretation(self, test_name, results):
        """
        Generates highly descriptive, statistically accurate interpretations 
        based on calculated values (means, variances, test statistics, and p-values).
        """
        # If results is already a clean pre-formatted string (e.g. from some confidence interval routes)
        if isinstance(results, str):
            clean_str = results.replace('\n', '<br>')
            return f"<strong>{test_name} Analysis Complete:</strong><br><br>{clean_str}"

        # If results is a dictionary structure
        if isinstance(results, dict):
            # Check for hypothesis testing (with p-value)
            p_value = results.get('p_value') or results.get('p')
            if p_value is not None:
                sig = "statistically significant" if p_value < 0.05 else "not statistically significant"
                t_stat_str = f" t-statistic of {results['t_stat']:.4f} and a" if 't_stat' in results else ""
                f_stat_str = f" F-statistic of {results['f_stat']:.4f} and a" if 'f_stat' in results else ""
                
                p_text = f"{p_value:.4f}" if p_value >= 0.0001 else "< 0.0001"
                
                desc = f"The {test_name} result is <strong>{sig}</strong> (p = {p_text}). "
                desc += f"Based on a calculated{t_stat_str}{f_stat_str} p-value of {p_text}, "
                if p_value < 0.05:
                    desc += "we reject the null hypothesis, indicating strong support for a meaningful group difference or association."
                else:
                    desc += "we fail to reject the null hypothesis, suggesting that observed differences may be due to sample variance."
                return desc

            # Check for descriptive/summary statistics
            if 'mean' in results:
                desc = f"<strong>{test_name} Summary:</strong><br>"
                desc += f"• The sample average is <strong>{results['mean']:.4f}</strong> with a standard deviation of <strong>{results['std_dev']:.4f}</strong> (n = {results['n']}).<br>"
                desc += f"• The distribution exhibits a skewness of <strong>{results['skewness']:.4f}</strong> and kurtosis of <strong>{results['kurtosis']:.4f}</strong>.<br>"
                if 'quartiles' in results and results['quartiles'].get('outliers'):
                    desc += f"• Identified {len(results['quartiles']['outliers'])} potential statistical outlier(s): {results['quartiles']['outliers']}."
                else:
                    desc += "• No statistical outliers were detected using the IQR rule."
                return desc

            # Generic dictionary formatting fallback
            parts = []
            for k, v in results.items():
                if k != 'assumptions' and not isinstance(v, (dict, list)):
                    clean_k = k.replace('_', ' ').title()
                    parts.append(f"• <strong>{clean_k}</strong>: {v}")
            if parts:
                return f"<strong>{test_name} Calculation Complete:</strong><br>" + "<br>".join(parts)

        return "Calculation complete. Please review the raw values above for your analysis."

    def get_apa_report(self, test_name, data_summary, results):
        """
        Drafts a perfect, APA 7th publication-ready results write-up using local Ollama.
        """
        prompt = f"""<|system|>
You are an Academic Journal Editor and Senior Statistical Methodologist.
Your task is to draft a flawless, publication-ready "Results and Analysis" section following the strict APA 7th edition manual guidelines.
Include all standard statistical notations (e.g., italicized letters like M, SD, t, F, p, d, r, df).
Use the exact statistical numbers from the calculated results below. Do not round numbers differently.
Provide exactly one highly detailed, academic paragraph. No headings, introductions, extra pleasantries, or markdown formatting blocks.

<|user|>
CALCULATION METRICS:
- Research Test: {test_name}
- Dataset Context: {data_summary}
- Calculated Results: {json.dumps(results, indent=2)}

APA 7TH FORMATTED WRITE-UP:
<|assistant|>
"""
        response = self._call_local_llm(prompt, temperature=0.1, max_tokens=4096)
        if response:
            return response
        if self.cloud_base_url:
            return "<strong>Notice:</strong> Cloud LLM service is currently unreachable or timed out. Please check your internet connection and API keys, or launch Ollama locally to enable local fallback."
        return "<strong>Notice:</strong> Local Ollama model is offline. Please launch Ollama and pull 'phi3.5' or 'llama3.1' to enable the Automated Academic Report Writer."

    def chat_tutor(self, message, test_name=None, results=None):
        """
        Generates an encouraging, technically solid explanation as an AI Stats Tutor.
        """
        context_str = ""
        if test_name and results:
            context_str = f"""
ACTIVE CALCULATION CONTEXT:
- Active Test: {test_name}
- Calculated Metrics: {json.dumps(results, indent=2)}
"""

        prompt = f"""<|system|>
You are an encouraging, expert Statistical Tutor and Research Mentor.
Help the researcher understand the concepts, interpret results, and write statistics code.
Structure your response cleanly using bold terms and bullet points. Avoid math jargon overload.
If code is requested, provide clean, copy-pasteable Python (using SciPy/pandas) or R blocks.
Keep explanations concise, educational, and direct.

{context_str}
<|user|>
{message}
<|assistant|>
"""
        response = self._call_local_llm(prompt, temperature=0.4, max_tokens=4096)
        if response:
            return response
        if self.cloud_base_url:
            return "The AI Stats Tutor is currently unreachable. Please check your network connection or API keys, or verify if local Ollama is active."
        return "The local AI Stats Tutor is currently resting. Please launch Ollama to continue learning."

    def profile_dataset(self, dataset_name, values):
        """
        Profiles a raw statistical array, flags anomalies, and plans which models to use.
        """
        if not values or not isinstance(values, list):
            return "No valid dataset array provided for profiling."

        # Compute preliminary stats to feed to LLM as strict constraints
        n = len(values)
        mean_val = sum(values) / n if n > 0 else 0
        min_val = min(values) if n > 0 else 0
        max_val = max(values) if n > 0 else 0

        prompt = f"""<|system|>
You are a Lead Data Scientist and Statistical Consultant.
Profile the given dataset array and provide an actionable statistical analysis and data cleaning plan.
Structure your report with exactly 3 sections using markdown:
1. 📊 DISTRIBUTION ANALYSIS: Analyze sample size (n={n}), average, scale, and skewness.
2. 🧹 DATA CLEANING PLAN: Detail outliers, repeats, or variance concerns, and clean/transformation recommendations.
3. 🔬 SUGGESTED MODELS: Explicitly recommend which statistical tests are most appropriate to run on this data and why.

Do not write conversational intros or outros. Provide clear, premium, bulleted markdown.

<|user|>
DATASET: {dataset_name}
RAW ARRAY VALUES: {values}
PRE-CALCULATIONS:
- Count (n): {n}
- Mean Value: {mean_val:.4f}
- Scale Range: {min_val} to {max_val}

PROFILE REPORT:
<|assistant|>
"""
        response = self._call_local_llm(prompt, temperature=0.2, max_tokens=4096)
        if response:
            return response
        if self.cloud_base_url:
            return "Unable to profile dataset. The Cloud LLM service is currently unreachable or timed out."
        return "Unable to profile dataset. Please verify that Ollama is active locally."
