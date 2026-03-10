import requests
import json

api_token = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTAwNDc0NSwiYWFpIjoxMSwidWlkIjoxMDA4MTI0NjEsImlhZCI6IjIwMjYtMDMtMTBUMDU6Mzc6MDkuMDAwWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTUzMTk0LCJyZ24iOiJhcHNlMiJ9.9fE59_EKMPSeirxzZLwwKdsnMTCWEF1VuyK-ReK7fwk"
endpoint = "https://api.monday.com/v2"

boards = [5027111612, 5027112113]

headers = {
    "Authorization": api_token,
    "Content-Type": "application/json",
    "API-Version": "2023-10"
}

results = {}

for board_id in boards:
    query = f"""
    query {{
      boards(ids: {board_id}) {{
        name
        columns {{
          id
          title
          type
        }}
      }}
    }}
    """
    response = requests.post(endpoint, json={"query": query}, headers=headers)
    results[board_id] = response.json()

print(json.dumps(results, indent=2))
