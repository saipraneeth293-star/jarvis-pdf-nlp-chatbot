# JARVIS Deployment Guide

## GitHub Repository

https://github.com/saipraneeth293-star/jarvis-pdf-nlp-chatbot

## Live Application

https://jarvis-pdf-nlp-chatbot-zeyjmchyxmwzdbplnudcsi.streamlit.app/

## 1. Local Test

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## 2. Push to GitHub

```powershell
git add .
git commit -m "Finalize JARVIS project"
git branch -M main
git push origin main
```

## 3. Deploy to Streamlit Community Cloud

Open:

https://share.streamlit.io/

Sign in with the GitHub account that owns the repository.

Create a new app using:

```text
Repository: saipraneeth293-star/jarvis-pdf-nlp-chatbot
Branch: main
Main file path: app.py
```

Click **Deploy**.

## 4. Public Access

The live application is:

https://jarvis-pdf-nlp-chatbot-zeyjmchyxmwzdbplnudcsi.streamlit.app/

Share this URL with your evaluator or users.

## 5. GitHub Profile Link

Add the live URL to the GitHub repository's **About / Website** field so visitors can open JARVIS directly from the repository page.

## 6. README

The `README.md` file contains the live demo link.

## 7. Updating the App

After making code changes:

```powershell
git add .
git commit -m "Update JARVIS"
git push origin main
```

The connected Streamlit deployment will use the updated repository.

## 8. Files That Should Be Committed

```text
app.py
requirements.txt
README.md
PROJECT_REPORT.md
GITHUB_DEPLOYMENT.md
.gitignore
```

Do not commit:

```text
venv/
.venv/
__pycache__/
*.pyc
*.pkl
*.pdf
.env
.streamlit/secrets.toml
```

## 9. Final Deployment Check

- GitHub repository opens ✅
- README contains the live link ✅
- Streamlit app opens ✅
- PDF upload works ✅
- PDF questions work ✅
- Summary works ✅
- Source pages appear ✅
