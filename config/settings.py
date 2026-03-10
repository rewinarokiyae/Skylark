import os
from dotenv import load_dotenv

# Load environment variables if .env file exists
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
MONDAY_API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTAwNDc0NSwiYWFpIjoxMSwidWlkIjoxMDA4MTI0NjEsImlhZCI6IjIwMjYtMDMtMTBUMDU6Mzc6MDkuMDAwWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTUzMTk0LCJyZ24iOiJhcHNlMiJ9.9fE59_EKMPSeirxzZLwwKdsnMTCWEF1VuyK-ReK7fwk"

# Endpoints
GROQ_ENDPOINT = "https://api.groq.com/openai/v1"
MONDAY_GRAPHQL_ENDPOINT = "https://api.monday.com/v2"

# Board IDs (Verified via API)
DEALS_BOARD_ID = 5027111612
WORK_ORDERS_BOARD_ID = 5027112113

# Default Model
GROQ_MODEL = "llama-3.3-70b-versatile"
