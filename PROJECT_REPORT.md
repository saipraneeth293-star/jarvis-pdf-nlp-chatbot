# JARVIS — Conversational PDF NLP Chatbot
## Final Project Report

### 1. Project Title

**JARVIS — Conversational PDF NLP Chatbot**

### 2. Abstract

JARVIS is a Python-based conversational chatbot with document intelligence. A user uploads a text-based PDF through a Streamlit interface and asks natural-language questions. The system extracts PDF text page by page, creates overlapping chunks, builds lightweight TF-IDF-style vectors, ranks relevant sections using cosine similarity, selects informative sentences, and returns an answer with source page references. JARVIS also provides an extractive summary and simple follow-up conversation context.

### 3. Problem Statement

Large PDF documents can be difficult to search manually. JARVIS provides a conversational interface that reduces the effort required to locate and understand information in uploaded documents.

### 4. Objectives

1. Build a Python conversational chatbot.
2. Apply NLP techniques to document search and user queries.
3. Support PDF upload and text extraction.
4. Retrieve relevant document passages.
5. Answer questions using retrieved information.
6. Provide document summaries.
7. Maintain short conversational context.
8. Deploy the application as a shareable Streamlit web app.

### 5. Technology Used

| Component | Technology |
|---|---|
| Programming language | Python |
| Web framework | Streamlit |
| PDF extraction | PyPDF |
| NLP retrieval | TF-IDF-style weighting |
| Similarity | Cosine similarity |
| Text processing | Regular expressions |
| Source control | GitHub |
| Deployment | Streamlit Community Cloud |

### 6. System Architecture

```text
User
  |
  v
Streamlit Interface
  |
  +--> PDF Upload
  |       |
  |       v
  |   Page-by-page extraction
  |       |
  |       v
  |   Text cleaning/chunking
  |       |
  |       v
  |   TF-IDF-style representation
  |       |
  |       v
  |   Cosine similarity
  |       |
  |       v
  |   Relevant passages
  |
  +--> User Question
          |
          v
      Conversation Context
          |
          v
      Retrieval / Summary
          |
          v
      JARVIS Response
```

### 7. Methodology

#### 7.1 PDF Extraction

The application reads each PDF page with PyPDF and stores the extracted text together with its page number.

#### 7.2 Text Chunking

Long page text is divided into overlapping chunks. Overlap helps preserve local context near chunk boundaries.

#### 7.3 NLP Retrieval

The application tokenizes text, removes common stop words, calculates TF-IDF-style term weights, and represents document chunks as sparse vectors.

#### 7.4 Similarity Ranking

The user question is represented using the same vocabulary. Cosine similarity compares the query representation with document chunk representations and ranks relevant chunks.

#### 7.5 Answer Generation

Relevant chunks are split into sentences. Sentences are ranked using query-word overlap and retrieval score. The strongest sentences are combined into the response.

#### 7.6 Summarization

Document sentences are scored using aggregate TF-IDF-style word importance. The highest-scoring sentences are selected and returned in their original order.

#### 7.7 Conversation Context

Simple follow-up questions containing references such as "it", "its", "this", or "those" are combined with the previous user question before document retrieval.

### 8. User Interface

The application includes:

- JARVIS online status
- PDF upload control
- Document status and statistics
- Page and chunk counts
- Chat interface
- Conversation history
- Clear conversation control
- Remove PDF control
- Question input
- Source page references

### 9. Testing Plan

| Test Case | Expected Result |
|---|---|
| Upload valid text PDF | Document becomes ready |
| Ask a document question | Relevant answer is returned |
| Ask a summary question | Document summary is generated |
| Ask a follow-up question | Previous topic is used as context |
| Remove PDF | PDF state is cleared |
| Clear conversation | Chat history is cleared |
| Upload an unreadable/scanned PDF | User receives a clear limitation message |
| Open deployed app | Streamlit interface loads |

### 10. Advantages

- Lightweight implementation.
- No external API key is required.
- Easy to understand and demonstrate.
- Suitable for an academic NLP chatbot project.
- Source page references improve traceability.
- Runs locally and on Streamlit Community Cloud.
- No large machine-learning model download is required.

### 11. Limitations

- Works best with selectable-text PDFs.
- Scanned PDFs require OCR.
- Lightweight retrieval is less semantic than embedding/LLM systems.
- Complex reasoning is limited.
- The current chatbot is retrieval-based rather than a generative LLM.

### 12. Future Enhancements

- OCR for scanned documents.
- Sentence-transformer embeddings.
- Retrieval-Augmented Generation (RAG).
- Local or hosted LLM integration.
- Multiple-document collections.
- Voice input and output.
- Persistent user accounts and chat history.
- Better citation highlighting.
- Multilingual support.

### 13. Deployment

**GitHub Repository**

https://github.com/saipraneeth293-star/jarvis-pdf-nlp-chatbot

**Live JARVIS Application**

`https://YOUR-STREAMLIT-APP.streamlit.app`

Replace the placeholder above with the actual Streamlit URL after successful deployment.

### 14. Conclusion

JARVIS demonstrates a practical Python and NLP approach to conversational document question answering. The project combines PDF processing, lightweight NLP retrieval, cosine similarity, summarization, conversation context, source-page tracking, and a Streamlit interface. The resulting application provides a clear foundation for an academic chatbot project and can be extended into a more advanced RAG or LLM-based assistant.
