import streamlit as st
import sys
import os

# Add parent directory to path to import agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.agent import BIAgent

# Page Configuration
st.set_page_config(
    page_title="Skylark Drones BI Agent",
    page_icon="🦅",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .insight-card {
        background-color: #1e1e26;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Agent
@st.cache_resource
def get_agent():
    return BIAgent()

agent = get_agent()

# Sidebar
with st.sidebar:
    st.title("🦅 Skylark BI")
    st.markdown("---")
    if st.button("Generate Leadership Summary"):
        with st.spinner("Generating weekly summary..."):
            summary = agent.get_weekly_summary()
            st.session_state.leadership_summary = summary

    st.markdown("### Data Sources")
    st.info("Connected to Monday.com API")
    st.info("Powered by Groq LLM")

# Main UI
st.title("Skylark Drones — Business Intelligence Agent")
st.markdown("---")

# Leadership Summary Display
if 'leadership_summary' in st.session_state:
    with st.expander("📊 Weekly Leadership Summary", expanded=True):
        st.markdown(st.session_state.leadership_summary)

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a business question..."):
    # Clear summary if new question asked (optional choice)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data and generating insights..."):
            result = agent.process_query(prompt)
            
            # Response formatting
            response_text = result['insight']
            
            # Show Metrics Detail internally in an expander for transparency
            with st.expander("View Analysis Details"):
                st.json(result['intent'])
                st.write("**Metric Data:**", result['metric_data'])
                if result['quality_issues']:
                    st.warning("**Data Quality Notes:**")
                    for issue in result['quality_issues']:
                        st.write(f"- {issue}")
            
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
