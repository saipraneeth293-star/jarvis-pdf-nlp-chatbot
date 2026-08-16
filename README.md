# 🤖 JARVIS — Conversational PDF NLP Chatbot

## 🚀 Live Demo

**[Open JARVIS Live](https://jarvis-pdf-nlp-chatbot-zeyjmchyxmwzdbplnudcsi.streamlit.app/)**

## 💻 GitHub Repository

https://github.com/saipraneeth293-star/jarvis-pdf-nlp-chatbot

## 📌 Project Overview

JARVIS is a Python-based conversational chatbot with PDF document intelligence. Users can upload a text-based PDF, ask questions about its contents, request a summary, ask follow-up questions, and receive source page references.

## ✨ Features

- 🤖 Conversational JARVIS interface
- 📄 PDF upload through the browser
- 📖 Page-aware PDF text extraction
- ✂️ Text chunking
- 🧠 Lightweight NLP retrieval
- 🔎 Similarity-based document search
- 💬 Chat history
- 📝 Extractive PDF summarization
- 🧠 Basic follow-up context
- 📑 Source page references
- ☁️ Streamlit Cloud deployment

## 🛠️ Technologies

- Python
- Streamlit
- PyPDF
- Lightweight TF-IDF-style retrieval
- Cosine similarity
- Regular expressions

## ▶️ Run Locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## 📂 Project Structure

```text
JARVIS/
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
├── GITHUB_DEPLOYMENT.md
└── .gitignore
```

## 📄 How to Use

1. Open the live JARVIS application.
2. Upload a text-based PDF.
3. Wait for **Document ready**.
4. Ask a question about the PDF.
5. Ask follow-up questions.
6. Ask `Summarize this PDF` for a document summary.
7. Check the source page shown with the answer.

## ⚠️ Limitations

- Best suited for selectable-text PDFs.
- Scanned/image-only PDFs require OCR.
- The current implementation is retrieval-based rather than a generative LLM.
- Complex semantic reasoning is limited.

## 🔮 Future Enhancements

- OCR
- Sentence-transformer embeddings
- RAG with an LLM
- Multiple-document search
- Voice input/output
- Persistent chat history
- Multilingual support
