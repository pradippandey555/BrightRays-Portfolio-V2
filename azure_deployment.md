# ☁️ Azure Deployment Guide (Final & Corrected)

This guide is specifically tailored to fix the **"Python Version Mismatch"** error (`libpython3.11.so.1.0: cannot open shared object file`) and ensure your **PDF generation** works on the Azure Student **Basic (B1)** plan.

---

## 🛑 Critical Fix: Python Version

Your logs showed that the **GitHub Builder** used **Python 3.11** to create the virtual environment, but your **Azure Web App** was trying to run it with **Python 3.10**.

**You MUST Ensure Both Match:**

1.  **Code Side**: I have already updated your `runtime.txt` to `python-3.11`.
2.  **Azure Portal Side** (Action Required):
    *   Go to [portal.azure.com](https://portal.azure.com) -> Your Web App -> **Configuration** -> **General Settings**.
    *   Change "Stack Settings" / "Python Version" to **Python 3.11**.
    *   Click **Save**.

---

## 🚀 Step 1: Deploy Latest Code

You have new code changes (PDF Tutorials, Runtime Fix, HTML Fix). Push them now:

```bash
git add .
git commit -m "Fix Azure runtime to 3.11 and add detailed project tutorials"
git push origin main
```

*Wait for the GitHub Action to complete.*

---

## ⚙️ Step 2: Verify Azure Configuration

Ensure these settings are correct in the **Azure Portal**:

1.  **Startup Command**:
    *   Go to **Configuration** -> **General settings**.
    *   **Startup Command**: `gunicorn --bind=0.0.0.0 --timeout 600 app:app`
    *   *Note: This command is critical for Flask apps.*

2.  **Environment Variables**:
    *   Go to **Configuration** -> **Application settings**.
    *   Ensure `SCM_DO_BUILD_DURING_DEPLOYMENT` is set to `true`.
    *   Ensure `MAIL_USERNAME`, `MAIL_PASSWORD`, `SECRET_KEY` are set.

---

## 🌐 Step 3: Custom Domain (Student Plan B1)

Since you are not using Render, here is how to use your domain `pradippandey555.com.np`.

**Prerequisite**: You must be on the **Basic (B1)** or **Shared (D1)** plan. The **Free (F1)** plan does NOT support this.

1.  Go to **Custom domains** in the Azure sidebar.
2.  Click **+ Add custom domain**.
3.  Enter: `pradippandey555.com.np`.
4.  Copy the **A Record** IP and **TXT Record** (Verification ID).
5.  Log in to your Domain Registrar or Cloudflare.
6.  Add the records:
    *   **Type**: `A` | **Name**: `@` | **Value**: `<Azure IP>`
    *   **Type**: `TXT` | **Name**: `asuid` | **Value**: `<Verification ID>`
    *   **Type**: `CNAME` | **Name**: `www` | **Value**: `pradippandey-portfolio.azurewebsites.net`
7.  Click **Validate** in Azure.

---

## ✅ Verification Checklist

1.  **Home Page**: Check that the "Technical Expertise" section loads (we fixed the `skill.items` error).
2.  **Projects**: Go to the **Projects Hub**. You should see detailed projects (Hydra, Cloud, etc.) instead of placeholders.
3.  **PDFs**: Click **"Download Case Study"** on any project. It should download a PDF containing the new "Implementation Steps / Tutorial" section we added.

---

## 🆘 Troubleshooting "Service Unavailable" (503 Error)

If your site abruptly stops working, it is likely due to a crash or a quota limit.

### 1. Check the Log Stream (Do this first!)
This tells us **exactly** why it crashed.
1.  Go to [portal.azure.com](https://portal.azure.com).
2.  Navigate to your Web App (`pradippandey555`).
3.  In the left sidebar, scroll down to **Monitoring** -> **Log Stream**.
4.  Watch the logs. Then, try to open your website in a new tab.
5.  **Copy and paste any Red Error Logs** you see into our chat.

### 2. Verify Startup Command
Azure sometimes forgets the command. Ensure it is set explicitly:
- Go to **Configuration** -> **General Settings**.
- **Startup Command**: `gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app`
- Click **Save**.

### 3. Restart the App Service
- Go to **Overview**.
- Click **Stop**, wait 10 seconds, then Click **Start**.
