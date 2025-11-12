# Custom Domain Deployment Guide: Digital Resonance Framework (DRF) Agent

This guide outlines the steps to deploy your Streamlit Capstone Project, the **Digital Resonance Framework (DRF) Agent**, and connect it to your custom domain, **DigitalInfluenceCore.com**.

The recommended approach is to use **Streamlit Community Cloud** for hosting and then configure your domain's DNS settings to point to the hosted application.

## Phase 1: Prepare and Deploy to Streamlit Community Cloud (Recap)

You must first complete the deployment to Streamlit Community Cloud, as outlined in the previous guide.

1.  **Create `requirements.txt`:** (Already done in the sandbox)
2.  **Create GitHub Repository:** Create a public repository (e.g., `drf-agent-capstone`) and upload all project files (`app.py`, `drf_agent.py`, `requirements.txt`, and the `knowledge_base` folder).
3.  **Secure API Key:** Set your `OPENAI_API_KEY` as a secret in the Streamlit Cloud dashboard.
4.  **Deploy App:** Deploy the app from your GitHub repository to Streamlit Community Cloud.

**Result of Phase 1:** Your app will be live at a Streamlit-provided URL, such as `[your-username]-[repo-name]-[hash].streamlit.app`.

## Phase 2: Configure Custom Domain (DigitalInfluenceCore.com)

Once your app is live on Streamlit Community Cloud, you can configure your custom domain.

### Step 2.1: Access Streamlit Cloud Settings

1.  Go to your Streamlit Community Cloud dashboard.
2.  Navigate to the settings for your deployed DRF Agent app.
3.  Look for the **Domains** or **Custom Domains** section.

### Step 2.2: Enter Your Custom Domain

1.  In the Custom Domains section, enter your desired domain or subdomain.
    *   **Option A (Subdomain):** `agent.digitalinfluencecore.com` (Recommended for a single app)
    *   **Option B (Root Domain):** `digitalinfluencecore.com` (Requires more complex setup)
2.  For this guide, we will use **Option A: `agent.digitalinfluencecore.com`**.

### Step 2.3: Update Your DNS Records

Streamlit Cloud will provide you with a **CNAME record** that you need to add to your domain's DNS settings. You will need to log in to your domain registrar (e.g., GoDaddy, Namecheap, Cloudflare) or DNS provider to do this.

| Record Type | Name/Host | Value/Target | TTL |
| :--- | :--- | :--- | :--- |
| **CNAME** | `agent` | `[your-streamlit-app-url].streamlit.app` | Automatic (or 3600) |

**Action:**
1.  Log in to the control panel for **DigitalInfluenceCore.com**.
2.  Find the **DNS Management** or **Zone Editor** section.
3.  Add a new **CNAME** record with the details provided by Streamlit Cloud.

### Step 2.4: Verification and Finalization

1.  After adding the CNAME record, return to the Streamlit Cloud Domains section.
2.  Click the **Verify** button.
3.  DNS changes can take up to 24 hours to propagate, but often happen within minutes.
4.  Once verified, Streamlit Cloud will automatically provision an SSL certificate (HTTPS) for your custom domain.

**Result of Phase 2:** Your DRF Agent will be permanently accessible at `https://agent.digitalinfluencecore.com`.

## Phase 3: Final Project Documentation (Module 6)

After deployment, the final step for your capstone project is to complete the documentation.

1.  **Final Capstone Report:** Write the report detailing the problem, the RAG-Agent architecture, the implementation, and the final deployment (including the custom domain).
2.  **Presentation Slides:** Prepare your presentation to showcase the live application and its business value to your soft skills training.

This deployment process fulfills the "Deployment strategies" learning outcome from **Module 5** and provides a professional, branded platform for your capstone project.
