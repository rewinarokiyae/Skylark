import requests
import json
import time

api_token = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTAwNDc0NSwiYWFpIjoxMSwidWlkIjoxMDA4MTI0NjEsImlhZCI6IjIwMjYtMDMtMTBUMDU6Mzc6MDkuMDAwWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTUzMTk0LCJyZ24iOiJhcHNlMiJ9.9fE59_EKMPSeirxzZLwwKdsnMTCWEF1VuyK-ReK7fwk"
endpoint = "https://api.monday.com/v2"

headers = {
    "Authorization": api_token,
    "Content-Type": "application/json",
    "API-Version": "2023-10"
}

# Deals Board: 5027111612
deals_mapping = {
    "name": "Deal Name",
    "text_mm1a61xw": "Owner code",
    "text_mm1aykvb": "Client Code",
    "status": "Deal Status",
    "date4": "Close Date (A)",
    "numeric_mm1aqm85": "Masked Deal value",
    "dropdown_mm1ah7tb": "Closure Probability",
    "date_mm1awe5n": "Tentative Close Date",
    "text_mm1aj877": "Deal Stage",
    "text_mm1aatyg": "Product deal",
    "text_mm1a3vjn": "Sector/service",
    "date_mm1ac61q": "Created Date"
}

# Work Orders Board: 5027112113
wo_mapping = {
    "name": "Deal name masked",
    "text_mm1apssz": "Customer Name Code",
    "text_mm1ax63n": "Serial #",
    "text_mm1acate": "Nature of Work",
    "text_mm1af65j": "Last executed month of recurring project",
    "color_mm1a6fyb": "Execution Status",
    "date_mm1a8adb": "Data Delivery Date",
    "date_mm1aye4k": "Date of PO/LOI",
    "text_mm1atzg9": "Document Type",
    "date_mm1ae33g": "Probable Start Date",
    "date_mm1a31qc": "Probable End Date",
    "text_mm1acajp": "BD/KAM Personnel code",
    "dropdown_mm1afvrf": "Sector",
    "text_mm1aq05p": "Type of Work",
    "text_mm1a8jpr": "Is any Skylark software platform part of the client deliverables in this deal?",
    "date_mm1a7wgk": "Last invoice date",
    "text_mm1avew2": "latest invoice no.",
    "numeric_mm1a280k": "Amount in Rupees (Excl of GST) (Masked)",
    "numeric_mm1aryxb": "Amount in Rupees (Incl of GST) (Masked)",
    "numeric_mm1ae8by": "Amount to be billed in Rs. (Exl. of GST) (Masked)",
    "numeric_mm1avdsd": "Amount to be billed in Rs. (Incl. of GST) (Masked)",
    "text_mm1a1wxx": "Quantity by Ops",
    "color_mm1agnn8": "Billing Status"
}

def update_column_title(board_id, column_id, new_title):
    query = """
    mutation ($boardId: ID!, $columnId: String!, $title: String!) {
      change_column_title (board_id: $boardId, column_id: $columnId, title: $title) {
        id
        title
      }
    }
    """
    variables = {
        "boardId": board_id,
        "columnId": column_id,
        "title": new_title
    }
    response = requests.post(endpoint, json={"query": query, "variables": variables}, headers=headers)
    return response.json()

print("Updating Deals Board Column Titles...")
for col_id, title in deals_mapping.items():
    print(f"Updating {col_id} -> {title}...")
    res = update_column_title(5027111612, col_id, title)
    print(json.dumps(res, indent=2))
    time.sleep(0.5)

print("\nUpdating Work Orders Board Column Titles...")
for col_id, title in wo_mapping.items():
    print(f"Updating {col_id} -> {title}...")
    res = update_column_title(5027112113, col_id, title)
    print(json.dumps(res, indent=2))
    time.sleep(0.5)

print("\nFinished updates.")
