import requests
from config import settings

class InsightGenerator:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = f"{settings.GROQ_ENDPOINT}/chat/completions"
        self.model = settings.GROQ_MODEL

    def generate_executive_report(self, query, traceability, metrics):
        """Generate a structured executive report matching strict formatting standards."""
        system_prompt = """
        You are a senior AI data engineer building a Business Intelligence Agent for executive decision support.
        Your goal is to answer founder-level business questions using retrieved board data.
        
        STRICT FORMATTING REQUIREMENTS:
        1. Title: A concise title starting with #.
        2. Format: If the 'Metrics' data is a list of structured records or dict, use a Markdown table. If it is a scalar value, dictionary containing a single value, or simple text string, write a bold narrative sentence instead of forcing a table.
        3. Insight: A strategic interpretation of the data. Identify patterns, interpret numbers, and highlight risks/opportunities.
        4. Data Source Verification: A clear block showing the source board, row count, and columns used.
        
        ANTI-HALLUCINATION RULES:
        - Never fabricate numbers.
        - Only use data provided in the Metrics block.
        - If no data is provided, state "Unable to generate results from retrieve data."
        """
        
        user_message = f"""
        User Question: {query}
        Metrics: {metrics}
        Traceability: {traceability}
        
        Generate the executive report now.
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Error generating report: {e}"

    def generate_leadership_summary(self, high_level_metrics, risk_indicators):
        """Generate a weekly leadership summary."""
        system_prompt = """
        You are the Skylark BI Agent. Generate a 'Weekly Leadership Summary' for the founder.
        Include sections:
        - Business Highlights
        - Sector Performance
        - Risk Indicators & Action Items
        """
        
        user_message = f"""
        Metrics: {high_level_metrics}
        Risks: {risk_indicators}
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Leadership Summary: {high_level_metrics}. Risks: {risk_indicators}"
