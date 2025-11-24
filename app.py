import streamlit as st
import os
import google.generativeai as genai
from drf_agent import DRFAgent # Import the Agent class

# --- Configuration ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(PROJECT_DIR, "knowledge_base")
FAISS_INDEX_FILE = os.path.join(KB_DIR, "drf_faiss_index.bin")

# --- Configure Gemini API Key from Streamlit Secrets ---
try:
    # Try to read from Streamlit secrets (for Streamlit Cloud deployment)
    gemini_api_key = st.secrets.get("GOOGLE_API_KEY")
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
        os.environ["GOOGLE_API_KEY"] = gemini_api_key
except Exception as e:
    # If secrets are not available, try environment variable (for local testing)
    if "GOOGLE_API_KEY" not in os.environ:
        st.error("Gemini API key not found. Please set GOOGLE_API_KEY in Streamlit secrets or environment variables.")

# --- Initialize Agent (Cached to run only once) ---
@st.cache_resource
def initialize_agent():
    """Initializes the DRFAgent and its RAG components."""
    if not os.path.exists(FAISS_INDEX_FILE):
        st.error("FAISS index not found. Please ensure Phase 1 was completed successfully.")
        return None
    try:
        agent = DRFAgent()
        return agent
    except Exception as e:
        st.error(f"Agent Initialization failed. Check the console for errors and ensure the FAISS index was created.")
        return None

agent = initialize_agent()

# --- Streamlit App Layout ---
st.set_page_config(
    page_title="DRF Communication Coach Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗣️ Digital Resonance Framework (DRF) Communication Coach")
st.subheader("AI Capstone Project: Real-time feedback based on proprietary framework.")

if agent:
    # Input Area
    st.markdown("---")
    st.markdown("### 1. Enter Your Communication Draft")
    user_input = st.text_area(
        "Paste your email, memo, or script here:",
        height=250,
        placeholder="e.g., 'Team, I need the Q3 report on my desk by 9 AM tomorrow. No excuses. Just get it done.'"
    )

    # Analysis Button
    if st.button("Analyze with DRF Agent", type="primary", use_container_width=True):
        if user_input:
            with st.spinner("DRF Agent is analyzing your draft..."):
                try:
                    # Call the agent's analysis method
                    feedback = agent.analyze_communication(user_input)
                    
                    st.markdown("---")
                    st.markdown("### 2. Agent Feedback (DRF Analysis)")
                    
                    # Display the structured feedback
                    st.markdown(feedback)
                    
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
        else:
            st.warning("Please enter a communication draft to analyze.")

    # Sidebar for Context
    st.sidebar.header("Project Context")
    st.sidebar.markdown(
        """
        This application is the IIT Patna Capstone Project, demonstrating:
        - **RAG (Module 1):** Injecting your DRF knowledge.
        - **AI Agents (Module 4):** Autonomous decision-making and tool use.
        - **App Building (Module 5):** Deployable, user-friendly interface.
        """
    )
    st.sidebar.info("The Agent's feedback is generated *only* from the knowledge provided in the manuscript PDF.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Powered by:** Gemini 2.5 Flash API")

else:
    st.error("Agent initialization failed. Check the console for errors and ensure the FAISS index was created.")
