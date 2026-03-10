import json
import requests
from config import settings

class QueryInterpreter:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = f"{settings.GROQ_ENDPOINT}/chat/completions"
        self.model = settings.GROQ_MODEL

    def interpret(self, user_query):
        """Interpret natural language query into a structured JSON object."""
        system_prompt = """
        You are a Business Intelligence Analyst. Your job is to extract search parameters from a user's question.
        You must return ONLY a JSON object with the following fields:
        - metric: (e.g., "pipeline_value", "revenue_by_sector", "delayed_projects", "completion_rate", "workload")
        - sector: (e.g., "energy", "mining", "powerline", "railways", "renewables", "all")
        - time_period: (e.g., "quarter", "month", "year", "all")
        - board_source: (e.g., "deals", "work_orders")

        Examples:
        "How is our mining pipeline looking this month?" -> {"metric": "pipeline_value", "sector": "mining", "time_period": "month", "board_source": "deals"}
        "Are there any delayed projects?" -> {"metric": "delayed_projects", "sector": "all", "time_period": "all", "board_source": "work_orders"}
        "Which sector has the highest workload?" -> {"metric": "workload", "sector": "all", "time_period": "all", "board_source": "work_orders"}
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content']
            return json.loads(content)
        except Exception as e:
            print(f"Error interpreting query: {e}")
            # Fault-tolerant fallback
            return {"metric": "pipeline_value", "sector": "all", "time_period": "all", "board_source": "deals"}
