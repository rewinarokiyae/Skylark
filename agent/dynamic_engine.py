import pandas as pd
import requests
import re
from config import settings

class DynamicEngine:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = f"{settings.GROQ_ENDPOINT}/chat/completions"
        self.model = settings.GROQ_MODEL

    def generate_and_execute(self, user_query, deals_df, wo_df):
        """
        Generates and executes a custom pandas pipeline using the LLM.
        """
        system_prompt = f"""
        You are an elite Python Data Scientist. A user has asked an arbitrary question about their datasets:
        Question: "{user_query}"

        You have access to two pandas DataFrames in your scope:
        1. `deals_df`
        Columns: {list(deals_df.columns)}

        2. `wo_df` (Work Orders)
        Columns: {list(wo_df.columns)}

        Your task is to write ONLY valid Python code using pandas to compute the exact answer to the user's question.
        You must assign the final extracted value (or dictionary/list of values) to a variable called `final_answer`.
        
        DO NOT explain your thought process. 
        DO NOT include python block markdown format ```python ... ```.
        Return ONLY raw Python code.

        Example output:
        filtered_df = deals_df[deals_df['Unified_Sector'] == 'Mining']
        avg_value = filtered_df['Masked Deal value'].mean()
        final_answer = {{"Average Mining Deal": avg_value}}
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
            ],
            "temperature": 0.0 # Deterministic code gen
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            generated_code = result['choices'][0]['message']['content']
            
            # Clean up markdown tags in case the LLM disobeys the prompt
            generated_code = re.sub(r"^```python\n", "", generated_code)
            generated_code = re.sub(r"^```\n", "", generated_code)
            generated_code = re.sub(r"\n```$", "", generated_code)
            
            # Local execution scope injection
            local_scope = {"deals_df": deals_df, "wo_df": wo_df, "pd": pd}
            
            # Execute dynamically generated script
            exec(generated_code, globals(), local_scope)
            
            if 'final_answer' in local_scope:
                return local_scope['final_answer']
            else:
                return "Error: LLM did not define 'final_answer' variable."
                
        except Exception as e:
            print(f"Dynamic execution failed: {e}")
            return f"Error computing custom metric: {e}"
