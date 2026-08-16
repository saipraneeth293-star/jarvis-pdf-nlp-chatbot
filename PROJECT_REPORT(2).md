# JARVIS — Conversational PDF NLP Chatbot
## Final Project Report

### 1. Project Title
**JARVIS — Conversational PDF NLP Chatbot**

### 2. Abstract
JARVIS is a Python-based conversational chatbot with document intelligence. A user uploads a text-based PDF through a Streamlit interface and asks natural-language questions. The system extracts PDF text page by page, creates overlapping chunks, builds lightweight TF-IDF-style representations, ranks relevant sections using cosine similarity, selects informative sentences, and returns an answer with source page references. JARVIS also provides extractive summarization and simple follow-up conversation context.

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
8. Deploy the application as a shareable web application.

### 5. Technologies Used

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
  |   NLP retrieval
  |       |
  |       v
  |   Similarity ranking
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
The application reads each PDF page and retains the page number with the extracted text.

#### 7.2 Text Chunking
Long page text is divided into overlapping chunks. The overlap helps preserve context near chunk boundaries.

#### 7.3 NLP Retrieval
Text is tokenized, common stop words are removed, term frequency and inverse-document-frequency style weights are calculated, and document chunks are represented as sparse vectors.

#### 7.4 Similarity Ranking
The question is converted into the same representation. Cosine similarity ranks the document chunks most related to the question.

#### 7.5 Answer Generation
Relevant chunks are split into sentences and ranked using query-word overlap and retrieval score. Strong sentences are combined into the answer.

#### 7.6 Summarization
Important sentences are selected using aggregate TF-IDF-style word importance and returned in their original order.

#### 7.7 Conversation Context
Simple follow-up questions containing references such as "it", "its", "this", or "those" are linked to the previous user question before retrieval.

### 8. User Interface

The application provides:
- JARVIS online status
- PDF uploader
- Document status
- Page and chunk statistics
- Chat interface
- Conversation history
- Clear conversation
- Remove PDF
- Source page references

### 9. Testing

| Test Case | Expected Result |
|---|---|
| Upload valid text PDF | Document becomes ready |
| Ask a document question | Relevant answer returned |
| Request a summary | Summary generated |
| Ask a follow-up | Previous topic is used as context |
| Remove PDF | Document state is cleared |
| Clear conversation | Chat history is cleared |
| Open live URL | JARVIS interface loads |

### 10. Advantages
- Lightweight implementation
- No external API key required
- Easy to demonstrate
- Suitable for an academic NLP chatbot
- Source page references
- Simple deployment
- No large model download

### 11. Limitations
- Works best with selectable-text PDFs.
- Scanned PDFs require OCR.
- Retrieval quality depends on lexical overlap.
- This is a retrieval-based chatbot rather than a generative LLM.

### 12. Future Enhancements
- OCR for scanned PDFs
- Sentence-transformer embeddings
- Retrieval-Augmented Generation
- LLM integration
- Multiple PDF collections
- Voice interface
- Persistent user history
- Multilingual support

### 13. Deployment

**GitHub Repository**

https://github.com/saipraneeth293-star/jarvis-pdf-nlp-chatbot

**Live JARVIS Application**

https://jarvis-pdf-nlp-chatbot-zeyjmchyxmwzdbplnudcsi.streamlit.app/

### 14. Conclusion
JARVIS demonstrates a practical Python and NLP approach to conversational document question answering. It combines PDF processing, lightweight NLP retrieval, similarity ranking, summarization, conversational context, source-page tracking, and a Streamlit interface. The deployed application provides a practical foundation for an academic chatbot project and can be extended into a more advanced RAG or LLM-based assistant.
