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
        - metric: (e.g., "pipeline_value", "revenue_by_sector", "top_clients", "delayed_projects", "completion_rate", "active_work_orders", "work_order_status_breakdown", "custom")
        - sector: (e.g., "energy", "mining", "powerline", "railways", "renewables", "all")
        - time_period: (e.g., "quarter", "month", "year", "all")
        - board_source: (e.g., "deals", "work_orders")

        IMPORTANT: If the user's question does NOT clearly fit one of the predefined metrics, you MUST classify the metric as "custom". It is critical that unique analytics requests trigger the custom routing.

        Examples:
        "Which clients have the largest deals?" -> {"metric": "top_clients", "sector": "all", "time_period": "all", "board_source": "deals"}
        "How is our mining pipeline looking this month?" -> {"metric": "pipeline_value", "sector": "mining", "time_period": "month", "board_source": "deals"}
        "Are there any delayed projects?" -> {"metric": "delayed_projects", "sector": "all", "time_period": "all", "board_source": "work_orders"}
        "How many work orders are currently active?" -> {"metric": "active_work_orders", "sector": "all", "time_period": "all", "board_source": "work_orders"}
        "How many work orders are completed vs in progress?" -> {"metric": "work_order_status_breakdown", "sector": "all", "time_period": "all", "board_source": "work_orders"}
        "What is the average deal size?" -> {"metric": "custom", "sector": "all", "time_period": "all", "board_source": "deals"}
        "Show me all details for the client with code COMPANY098" -> {"metric": "custom", "sector": "all", "time_period": "all", "board_source": "deals"}
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
