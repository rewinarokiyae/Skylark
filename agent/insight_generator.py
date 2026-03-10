import requests
from config import settings

class InsightGenerator:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = f"{settings.GROQ_ENDPOINT}/chat/completions"
        self.model = settings.GROQ_MODEL

    def generate_insight(self, query_interpretation, metrics, data_issues=None):
        """Convert metrics and data issues into a conversational executive insight."""
        system_prompt = """
        You are a sophisticated Business Intelligence AI for Skylark Drones.
        Your goal is to provide founder-level insights.
        Convert the provided raw metrics and data quality issues into a conversational, professional, and clear executive summary.
        - Be concise.
        - Highlight risks (e.g., missing data, delayed projects).
        - Use a helpful, confident tone.
        - Don't just list numbers; explain what they mean for the business.
        """
        
        user_message = f"""
        Context:
        - Query Goal: {query_interpretation}
        - Metrics Found: {metrics}
        - Data Issues: {data_issues if data_issues else 'None detected'}
        
        Generate a conversational insight response.
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
            return f"I analyzed the data and found the following: {metrics}. (Note: Insight generation failed due to {e})"

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
