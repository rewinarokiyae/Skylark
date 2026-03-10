import os
from dotenv import load_dotenv

# Load environment variables if .env file exists
load_dotenv()

# API Keys (provided in prompt)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY", "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTAwNDc0NSwiYWFpIjoxMSwidWlkIjoxMDA4MTI0NjEsImlhZCI6IjIwMjYtMDMtMTBUMDU6Mzc6MDkuNDk5WiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTUzMTk0LCJyZ24iOiJhcHNlMiJ9.GMoRk3pxrCnjtUfBqHnUo1sHFZay1dqr-Nt8SjkDDaA")

# Endpoints
MONDAY_GRAPHQL_ENDPOINT = "https://api.monday.com/v2"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1"

# Board IDs (In a real scenario, these would be fetched or configured)
# For the prototype, we assume we might need to find them or use names
DEALS_BOARD_NAME = "Deals"
WORK_ORDERS_BOARD_NAME = "Work Orders"

# Default Model
GROQ_MODEL = "llama-3.3-70b-versatile"
