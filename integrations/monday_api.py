import requests
import pandas as pd
from config import settings

class MondayClient:
    def __init__(self):
        self.api_token = settings.MONDAY_API_TOKEN
        self.endpoint = settings.MONDAY_GRAPHQL_ENDPOINT
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            "API-Version": "2023-10"
        }

    def fetch_board_items(self, board_id):
        """Fetch all items and their column values from a specific board."""
        query = f"""
        query {{
          boards(ids: {board_id}) {{
            items_page {{
              items {{
                id
                name
                column_values {{
                  column {{
                    title
                  }}
                  text
                }}
              }}
            }}
          }}
        }}
        """
        response = requests.post(self.endpoint, json={"query": query}, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Monday API Request failed: {response.status_code} - {response.text}")
            
        data = response.json()
        if "errors" in data:
            raise Exception(f"Monday API Error: {data['errors']}")
            
        if not data["data"]["boards"]:
            raise Exception(f"Board {board_id} not found or access denied.")
            
        board_data = data["data"]["boards"][0]
        items = board_data["items_page"]["items"]
        
        # Flatten column values into a list of dicts
        flattened_items = []
        for item in items:
            row = {
                "Item ID": item["id"],
                "Item Name": item["name"]
            }
            for col in item["column_values"]:
                title = col["column"]["title"]
                row[title] = col["text"]
            flattened_items.append(row)
            
        return pd.DataFrame(flattened_items)

    def get_deals_board_data(self):
        """Fetch data from the Deals board."""
        return self.fetch_board_items(settings.DEALS_BOARD_ID)

    def get_work_orders_board_data(self):
        """Fetch data from the Work Orders board."""
        return self.fetch_board_items(settings.WORK_ORDERS_BOARD_ID)
