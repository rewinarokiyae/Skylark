import requests
import json
import pandas as pd
from config import settings

class MondayClient:
    def __init__(self):
        self.api_key = settings.MONDAY_API_KEY
        self.url = settings.MONDAY_GRAPHQL_ENDPOINT
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def execute_graphql_query(self, query, variables=None):
        """Execute a GraphQL query on the Monday.com API."""
        data = {"query": query}
        if variables:
            data["variables"] = variables
        
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code != 200:
            raise Exception(f"GraphQL Query failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL Query returned errors: {result['errors']}")
            
        return result

    def get_board_id_by_name(self, board_name):
        """Helper to find board ID by name."""
        query = """
        query {
            boards (limit: 50) {
                id
                name
            }
        }
        """
        result = self.execute_graphql_query(query)
        boards = result["data"]["boards"]
        for board in boards:
            if board["name"].lower() == board_name.lower():
                return board["id"]
        return None

    def fetch_board_items(self, board_id):
        """Fetch all items and column values from a board."""
        query = """
        query ($board_id: [ID]) {
            boards (ids: $board_id) {
                items_page (limit: 500) {
                    items {
                        id
                        name
                        column_values {
                            id
                            text
                            column {
                                title
                            }
                        }
                    }
                }
            }
        }
        """
        variables = {"board_id": [board_id]}
        result = self.execute_graphql_query(query, variables)
        
        items = result["data"]["boards"][0]["items_page"]["items"]
        
        # Flatten structure for pandas
        rows = []
        for item in items:
            row = {"item_id": item["id"], "name": item["name"]}
            for col_val in item["column_values"]:
                col_title = col_val["column"]["title"].lower().replace(" ", "_")
                row[col_title] = col_val["text"]
            rows.append(row)
            
        return pd.DataFrame(rows)

    def get_deals_board_data(self):
        """Fetch and return Deals board data."""
        board_id = self.get_board_id_by_name(settings.DEALS_BOARD_NAME)
        if not board_id:
            # Fallback for prototype if board not found - try common names or ID search
            # In production, we'd want IDs to be configured or discovered reliably
            print(f"Warning: Board '{settings.DEALS_BOARD_NAME}' not found.")
            return pd.DataFrame() # Return empty for now
        return self.fetch_board_items(board_id)

    def get_work_orders_board_data(self):
        """Fetch and return Work Orders board data."""
        board_id = self.get_board_id_by_name(settings.WORK_ORDERS_BOARD_NAME)
        if not board_id:
            print(f"Warning: Board '{settings.WORK_ORDERS_BOARD_NAME}' not found.")
            return pd.DataFrame()
        return self.fetch_board_items(board_id)
