# Decision Log - Skylark BI Agent

## Architectural Strategy
- **Modularity**: Separating API logic, data processing, and AI orchestration.
- **Resilience**: The `data_cleaner.py` is central to handling the "messy" real-world data issues.
- **LLM Selection**: Using Groq's high-speed API for both query interpretation and insight generation to ensure low latency for the founder.

## Key Decisions
1. **Normalization**: Sector names and date formats are standardizing in a dedicated layer before metrics are calculated.
2. **Tabular Processing**: Converting Monday.com GraphQL JSON responses to Pandas DataFrames early in the pipeline.
3. **Conversational Interface**: Streamlit selected for rapid prototype development and built-in interactivity.
