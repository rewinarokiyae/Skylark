# Skylark Drones — Monday.com Business Intelligence Agent

An AI agent that answers founder-level business questions by analyzing data stored in monday.com boards.

## Features
- Dynamic Monday.com Integration (GraphQL).
- Natural Language Question Understanding (Groq LLM).
- Business Intelligence Engine (Pandas).
- Automated Insight Generation (Groq LLM).
- Conversational Dashboard (Streamlit).
- Leadership Summary Updates.

## Setup Instructions
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env` or use `config/settings.py`:
   - `MONDAY_API_KEY`
   - `GROQ_API_KEY`
4. Run the application:
   ```bash
   streamlit run ui/app.py
   ```

## Project Structure
- `agent/`: Core AI agent logic.
- `integrations/`: Monday.com API interaction.
- `processing/`: Data cleaning and analytics.
- `ui/`: Streamlit dashboard.
- `config/`: Configuration and settings.
