# Capstone Project Report: Digital Resonance Framework (DRF) Communication Coach Agent

**Course:** IIT Patna Certificate Course on Generative AI
**Module Focus:** Module 1 (LLMs & RAG), Module 4 (AI Agents), Module 5 (App Building)
**Author:** Manus AI (on behalf of the User)
**Date:** November 3, 2025

## 1. Executive Summary

The **Digital Resonance Framework (DRF) Communication Coach Agent** is a capstone project that successfully applies advanced Generative AI concepts to the domain of corporate soft skills training. The project's core innovation is the use of **Retrieval-Augmented Generation (RAG)** to inject the user's proprietary knowledge—the Digital Resonance Framework (DRF) and Digital Emotional Intelligence (DEQ) principles—into a Large Language Model (LLM). The resulting AI Agent acts as a real-time communication coach, providing structured, framework-based feedback on digital communication drafts. This project demonstrates proficiency in RAG implementation, AI Agent design, and the deployment of an AI-powered web application.

## 2. Problem Statement

In the modern corporate environment, leadership communication is increasingly mediated by digital channels (email, chat, memos). The nuances of emotional intelligence (EQ) and tone are often lost, leading to miscommunication, reduced team morale, and decreased productivity. The user, a corporate soft skills trainer specializing in the DRF and DEQ, requires a scalable, automated tool to:
1.  **Codify and leverage** their proprietary DRF knowledge.
2.  **Provide instant, objective feedback** on communication drafts based on DRF principles.
3.  **Demonstrate the practical application** of Generative AI in the soft skills and leadership development space.

## 3. Technical Architecture and Implementation

The project follows a three-part architecture: the Knowledge Base (RAG), the Agent Logic, and the Application Interface.

### 3.1. Knowledge Base (Module 1: LLMs & RAG)

The RAG system is the foundation of the Agent's expertise, ensuring all feedback is grounded in the DRF.

| Component | Technology/Method | Purpose |
| :--- | :--- | :--- |
| **Source Data** | User's proprietary manuscript (PDF) | Contains the full text of the Digital Resonance Framework and DEQ principles. |
| **Data Pre-processing** | Python (`pdftotext`, custom script) | Extracted text from PDF and performed heuristic chunking, resulting in **422 knowledge chunks** to maintain context integrity. |
| **Embedding Model** | `all-MiniLM-L6-v2` (Sentence Transformers) | Converts text chunks and user queries into high-dimensional vector embeddings. |
| **Vector Store** | **FAISS** (Facebook AI Similarity Search) | Stores the vector embeddings for fast, efficient similarity search (retrieval). |
| **Retrieval** | L2 distance search (k=5) | Finds the top 5 most relevant DRF principles/chunks for any given query. |

### 3.2. Agent Logic (Module 4: AI Agents)

The Agent is responsible for orchestrating the RAG process and structuring the final output.

| Component | Technology/Method | Purpose |
| :--- | :--- | :--- |
| **LLM** | `gpt-4.1-mini` (via OpenAI API) | Used for complex reasoning, synthesis, and structured output generation. |
| **System Prompt** | Detailed Prompt Engineering | Defines the Agent's persona ("Executive Communication Coach") and enforces a strict, four-part output format (Score, Summary, 3 Actionable Points, Reference). |
| **Tool Use** | Internal `DRFKnowledgeBase` tool | The Agent is prompted to use the RAG system to retrieve context before generating the final analysis, ensuring the response is grounded in the user's IP. |

### 3.3. Application Interface (Module 5: App Building)

The application provides a user-friendly interface for interacting with the Agent.

| Component | Technology/Method | Purpose |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | Provides a simple, interactive web interface with a text area for input and a dedicated section for the Agent's structured output. |
| **Backend** | Python | Handles the Streamlit application logic, initializes the `DRFAgent`, and manages the API calls. |
| **Deployment** | Streamlit Community Cloud (Planned) | Chosen for its ease of use, free tier, and direct integration with GitHub, fulfilling the course requirement for deployment strategy. |

## 4. Testing and Validation

The Agent was validated using high-stakes communication drafts to ensure the RAG system provided relevant context and the LLM adhered to the structured output format.

| Test Case | Digital Resonance Score | Key Finding |
| :--- | :--- | :--- |
| **Aggressive/Urgent Email** | 4/10 | Agent correctly identified the lack of Digital Self-Regulation and recommended reframing the tone with respect to the DRF. |
| **Balanced/Collaborative Email** | 7/10 | Agent provided nuanced feedback, suggesting improvements in clarity and emotional connection, demonstrating a high level of synthesis. |
| **Sensitive Restructuring Announcement** | 6/10 | Agent correctly identified the need for greater **Emotional Validation** and **Digital Social Awareness** in the sensitive announcement, citing the DRF principles on recognizing emotional triggers. |

## 5. Conclusion and Future Work

The **DRF Communication Coach Agent** is a successful capstone project that demonstrates mastery of the Generative AI course material. It transforms the user's intellectual property into a scalable, automated coaching product.

**Future Enhancements:**
1.  **Multi-Modal Input (Module 2):** Extend the Agent to analyze transcripts of video calls or voice notes for tone and pace, leveraging multi-modal AI techniques.
2.  **Agentic Workflow (Module 4):** Implement a more complex Agent workflow where a secondary "Refinement Agent" checks the output of the primary Agent for tone and adherence to the user's specific voice.
3.  **User Authentication (Web Development):** Integrate user login to track individual communication patterns and provide longitudinal coaching insights.

This project serves as a powerful portfolio piece, showcasing the ability to bridge advanced AI technology with specialized domain expertise to create a high-value business solution.
