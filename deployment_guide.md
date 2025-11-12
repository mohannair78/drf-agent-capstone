# Permanent Deployment Guide: Digital Resonance Framework (DRF) Agent

This guide outlines the steps required to permanently deploy your Streamlit Capstone Project, the **Digital Resonance Framework (DRF) Agent**, using **Streamlit Community Cloud**. This platform is ideal for hosting Streamlit applications for free.

## Prerequisites

1.  **GitHub Account:** You must have a GitHub account.
2.  **Streamlit Community Cloud Account:** You must sign up for a free account at [https://streamlit.io/cloud](https://streamlit.io/cloud).
3.  **Project Files:** You need all the files created in the sandbox:
    *   `app.py` (The Streamlit application)
    *   `drf_agent.py` (The Agent logic)
    *   `create_vector_db.py` (Not strictly needed for deployment, but good for reference)
    *   `knowledge_base/drf_faiss_index.bin` (The vector index)
    *   `knowledge_base/drf_chunks_list.txt` (The list of chunks)
    *   `requirements.txt` (A list of all required Python packages)

## Step 1: Create the `requirements.txt` File

Your application relies on several Python packages. You need to create a `requirements.txt` file that lists them all so Streamlit Cloud can install them.

**Required Packages:**
*   `streamlit`
*   `openai`
*   `faiss-cpu`
*   `sentence-transformers`
*   `numpy`

**Action:** Create the `requirements.txt` file in your project root (`/home/ubuntu/drf_agent_project/`).

```bash
# In the sandbox terminal:
echo "streamlit" > /home/ubuntu/drf_agent_project/requirements.txt
echo "openai" >> /home/ubuntu/drf_agent_project/requirements.txt
echo "faiss-cpu" >> /home/ubuntu/drf_agent_project/requirements.txt
echo "sentence-transformers" >> /home/ubuntu/drf_agent_project/requirements.txt
echo "numpy" >> /home/ubuntu/drf_agent_project/requirements.txt
```

## Step 2: Prepare the Project for GitHub

Streamlit Community Cloud deploys directly from a GitHub repository.

### 2.1 Create a GitHub Repository

1.  Go to [https://github.com/new](https://github.com/new) and create a new public repository (e.g., `drf-agent-capstone`).
2.  Initialize it with a `README.md` and a `.gitignore` file.

### 2.2 Upload Project Files

You need to upload the following files and the `knowledge_base` folder to your new GitHub repository:

*   `app.py`
*   `drf_agent.py`
*   `requirements.txt`
*   **Folder:** `knowledge_base/` (Must contain `drf_faiss_index.bin` and `drf_chunks_list.txt`)

**Note:** The vector index (`drf_faiss_index.bin`) and the chunks list (`drf_chunks_list.txt`) are crucial. Ensure they are uploaded, even if they are large.

## Step 3: Secure Your OpenAI API Key

Your `drf_agent.py` uses the `openai` library, which requires an API key. You must secure this key on Streamlit Cloud.

1.  Go to your Streamlit Community Cloud dashboard.
2.  Select **Settings** for your app (or during the deployment process).
3.  Navigate to the **Secrets** section.
4.  Add your OpenAI API key in the following format:

```ini
# .streamlit/secrets.toml
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Note:** Your `drf_agent.py` script needs a small modification to read this secret.

**Action:** Modify `drf_agent.py` to use the Streamlit secret.

```python
# In drf_agent.py, replace the line:
# client = OpenAI()

# With the following code to read the key from Streamlit secrets:
import streamlit as st
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
```

## Step 4: Deploy on Streamlit Community Cloud

1.  Log in to your Streamlit Community Cloud account.
2.  Click the **New App** button.
3.  Select your GitHub repository (`drf-agent-capstone`).
4.  **Main file path:** `app.py`
5.  Click **Deploy!**

Streamlit Cloud will automatically clone your repository, install the packages from `requirements.txt`, and run your `app.py`. Your application will be live at a permanent URL (e.g., `[your-username]-[repo-name]-[hash].streamlit.app`).

## Final Step: Clean Up

Once your application is successfully deployed on Streamlit Cloud, you can safely terminate the sandbox session, as your capstone project will be permanently hosted on the new platform.

This deployment process fulfills the "Deployment strategies (e.g., cloud platforms)" learning outcome from **Module 5** of your course.
