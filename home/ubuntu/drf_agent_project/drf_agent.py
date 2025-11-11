import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# --- Configuration ---
MODEL_NAME = 'all-MiniLM-L6-v2'
PROJECT_DIR = "/home/ubuntu/drf_agent_project"
KB_DIR = os.path.join(PROJECT_DIR, "knowledge_base")
FAISS_INDEX_FILE = os.path.join(KB_DIR, "drf_faiss_index.bin")
CHUNKS_LIST_FILE = os.path.join(KB_DIR, "drf_chunks_list.txt")

# Initialize OpenAI client (for sandbox testing)
import streamlit as st
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- RAG Tool Implementation (from Phase 1) ---

class DRFKnowledgeBase:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(FAISS_INDEX_FILE)
        with open(CHUNKS_LIST_FILE, 'r', encoding='utf-8') as f:
            self.chunks = f.read().split('\n---\n')

    def retrieve_context(self, query, k=3):
        """Retrieves the top k most relevant chunks for a given query."""
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, k)
        retrieved_chunks = [self.chunks[i] for i in I[0]]
        return "\n\n".join(retrieved_chunks)

# --- Agent Implementation (Phase 2) ---

class DRFAgent:
    def __init__(self):
        self.kb = DRFKnowledgeBase()
        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self):
        """Crafts the detailed system prompt for the LLM Agent."""
        return """
You are the 'Executive Communication Coach,' an AI Agent specializing in Leadership Communication, Digital Emotional Intelligence (DEQ), and the Digital Resonance Framework (DRF).
Your goal is to analyze a user's communication draft and provide structured, actionable feedback based *only* on the knowledge provided by your RAG tool.

**Your Persona and Rules:**
1. **Role:** Executive Communication Coach. Your tone must be professional, encouraging, and authoritative.
2. **Knowledge Source:** You MUST use the `DRFKnowledgeBase` tool to retrieve relevant context before formulating your response. Do not use external knowledge.
3. **Analysis:** Analyze the user's text for clarity, tone, emotional intelligence (DEQ), and alignment with the DRF principles.
4. **Output Format:** Your response MUST be structured as follows:
    a. **Digital Resonance Score (1-10):** A single number assessing the overall effectiveness and DEQ alignment of the communication.
    b. **Analysis Summary:** A brief paragraph explaining the score based on DRF principles.
    c. **Actionable Feedback (3 Points):** A bulleted list of exactly three specific, actionable suggestions for improvement, citing the relevant DRF principle (e.g., "Improve clarity by focusing on Digital Self-Regulation: Boundary Management").
    d. **DRF Principle Reference:** A brief quote or summary of the most relevant DRF principle from the retrieved context.

**Tool Description:**
- **Tool Name:** `DRFKnowledgeBase`
- **Function:** `retrieve_context(query: str)`
- **Purpose:** Use this tool to search the Digital Resonance Framework knowledge base. Your query should be a question that helps you find the specific DRF principles needed to analyze the user's communication.
"""

    def analyze_communication(self, user_communication):
        """Runs the RAG-Agent pipeline to analyze the user's communication."""
        
        # 1. Agent decides on the RAG query (based on the user's input)
        rag_query = "Summarize the core principles of the Digital Resonance Framework and Digital Emotional Intelligence."
        
        # 2. Agent calls the RAG tool
        retrieved_context = self.kb.retrieve_context(rag_query, k=5) # Retrieve 5 chunks for richer context
        
        # 3. Agent formulates the final prompt to the LLM
        full_prompt = f"""
{self.system_prompt}

**Retrieved DRF Knowledge (from RAG Tool):**
---
{retrieved_context}
---

**User Communication Draft to Analyze:**
---
{user_communication}
---

Please analyze the User Communication Draft and provide your structured feedback based *only* on the provided DRF Knowledge.
"""
        
        # 4. LLM call to generate the final response
        print("Sending analysis request to LLM...")
        response = client.chat.completions.create(
            model="gpt-4.1-mini", # Using a capable model for complex reasoning
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_prompt}
            ]
        )
        
        return response.choices[0].message.content

if __name__ == "__main__":
    try:
        agent = DRFAgent()
        
        # --- Test Communication Drafts ---
        draft_1 = """
Subject: URGENT: Need that report ASAP!
Team, I need the Q3 report on my desk by 9 AM tomorrow. No excuses. This is a priority and I don't have time to chase people down. Just get it done.
- [Leader's Name]
"""
        
        print("="*80)
        print("ANALYZING DRAFT 1: Aggressive/Urgent Email")
        print("="*80)
        feedback_1 = agent.analyze_communication(draft_1)
        print(feedback_1)
        
        draft_3 = """
Subject: Important Update Regarding Company Structure
Team, as part of our ongoing commitment to efficiency and market responsiveness, we are announcing a necessary restructuring, effective immediately. This decision was made after careful consideration by the leadership team to ensure the long-term viability of the company. We understand this news may cause uncertainty, but we are confident this is the right direction. More details will be shared by your direct managers in the coming days. Please direct all immediate questions to your department head.
— The Leadership Team
"""

        print("\n\n"+"="*80)
        print("ANALYZING DRAFT 3: Sensitive Restructuring Announcement")
        print("="*80)
        feedback_3 = agent.analyze_communication(draft_3)
        print(feedback_3)

        draft_2 = """
Subject: Quick check-in on the Q3 report
Hi Team,
I hope you're all having a productive week. I wanted to quickly check in on the Q3 report. I know everyone is busy, but it would be helpful to have it by tomorrow morning so I can review it before the leadership meeting. Please let me know if there are any roadblocks I can help clear. Thanks!
- [Leader's Name]
"""
        
        print("\n\n"+"="*80)
        print("ANALYZING DRAFT 2: Balanced/Collaborative Email")
        print("="*80)
        feedback_2 = agent.analyze_communication(draft_2)
        print(feedback_2)
        
    except Exception as e:
        print(f"An error occurred during Agent execution: {e}")
