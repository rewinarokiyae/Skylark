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

# Custom Styling for Premium Look
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(0, 0, 0) 0%, rgb(6, 6, 12) 90.2%);
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #00d4ff 0%, #00ffaa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .insight-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
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
    st.image("https://www.skylarkdrones.com/images/logo.png", width=200) # Placeholder for branding
    st.title("BI Intelligence")
    st.markdown("---")
    if st.button("Generate Weekly Summary"):
        with st.spinner("Analyzing operational trends..."):
            summary = agent.get_weekly_summary()
            st.session_state.leadership_summary = summary

    st.markdown("### 🔌 Core Connectors")
    st.success("Monday.com Pipeline")
    st.success("Groq Intelligence (Llama 3.3)")

# Main Header
st.title("Skylark Drones — BI Agent")
st.caption("Founder-level insights powered by real-time Monday.com data")

# Summary Expandable
if 'leadership_summary' in st.session_state:
    with st.expander("📝 Strategic Leadership Summary", expanded=True):
        st.markdown(st.session_state.leadership_summary)

# Chat Hub
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome back. I've refreshed the data from Monday.com boards. How can I help you analyze the pipeline or work orders today?"}
    ]

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Agent
if prompt := st.chat_input("Ask about deals, revenue, or project delays..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Querying Monday.com & calculating metrics..."):
            result = agent.process_query(prompt)
            
            # Response formatting
            if "error" in result:
                response_text = result["error"]
                st.error("Validation Failed: Data could not be retrieved from Monday.com.")
                with st.expander("🛠️ Traceability Details"):
                    st.write("**Traceability:**", result.get('traceability', {}))
            else:
                response_text = result['report']
                
                # Technical Debug/Details
                with st.expander("🛠️ Analytics Breakdown"):
                    st.write("**Intent Extraction:**", result.get('intent', {}))
                    st.write("**Calculated Metric:**", result.get('metric_data', {}))
                    st.write("**Traceability:**", result.get('traceability', {}))
            
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
