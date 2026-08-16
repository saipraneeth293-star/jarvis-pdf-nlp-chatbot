import re
import streamlit as st
from pypdf import PdfReader



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "messages": [],
    "pdf_name": "",
    "pdf_text": "",
    "chunks": [],
    "vectorizer": None,
    "matrix": None,
    "page_count": 0
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# HEADER
# ============================================================

st.success("🟢 JARVIS ONLINE")

st.title("🤖 JARVIS")

st.caption(
    "Intelligent conversational AI assistant "
    "with PDF document intelligence"
)

st.divider()


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    try:

        reader = PdfReader(uploaded_file)

        pages = []

        for page in reader.pages:

            try:

                text = page.extract_text()

                if text:

                    text = text.strip()

                    if text:
                        pages.append(text)

            except Exception:
                continue

        return "\n\n".join(pages), len(reader.pages)

    except Exception as error:

        st.error(
            f"Could not load PDF: {error}"
        )

        return "", 0


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CREATE DOCUMENT CHUNKS
# ============================================================

def create_chunks(
    text,
    chunk_size=1200,
    overlap=200
):

    text = clean_text(text)

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# ============================================================
# BUILD TF-IDF SEARCH ENGINE
# ============================================================

def build_search_engine(chunks):

    if not chunks:
        return None, None

    try:

        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=15000
        )

        matrix = vectorizer.fit_transform(chunks)

        return vectorizer, matrix

    except Exception as error:

        st.error(
            f"Could not build search engine: {error}"
        )

        return None, None


# ============================================================
# SEARCH DOCUMENT
# ============================================================

def search_document(
    question,
    top_k=5
):

    if (
        not st.session_state.chunks
        or st.session_state.vectorizer is None
        or st.session_state.matrix is None
    ):
        return []

    try:

        query_vector = (
            st.session_state.vectorizer
            .transform([question])
        )

        similarities = cosine_similarity(
            query_vector,
            st.session_state.matrix
        )[0]

        ranked_indices = similarities.argsort()[::-1]

        results = []

        for index in ranked_indices[:top_k]:

            score = float(
                similarities[index]
            )

            if score > 0:

                results.append(
                    {
                        "text":
                            st.session_state.chunks[index],

                        "score":
                            score
                    }
                )

        return results

    except Exception:

        return []


# ============================================================
# SENTENCE SPLITTER
# ============================================================

def split_sentences(text):

    return [
        sentence.strip()
        for sentence in re.split(
            r"(?<=[.!?])\s+",
            text
        )
        if len(sentence.strip()) > 20
    ]


# ============================================================
# DOCUMENT SUMMARIZATION
# ============================================================

def summarize_document(
    text,
    sentence_count=7
):

    if not text:

        return (
            "There is no document available "
            "to summarize."
        )

    sentences = split_sentences(text)

    if not sentences:

        return (
            "I could not find enough readable text "
            "to create a summary."
        )

    if len(sentences) <= sentence_count:

        return " ".join(sentences)

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            sentences
        )

        word_scores = matrix.sum(
            axis=0
        ).A1

        sentence_scores = (
            matrix @ word_scores
        ).A1

        ranked = sorted(
            range(len(sentences)),
            key=lambda i:
                sentence_scores[i],
            reverse=True
        )

        selected_indices = sorted(
            ranked[:sentence_count]
        )

        summary = [
            sentences[index]
            for index in selected_indices
        ]

        return " ".join(summary)

    except Exception:

        return " ".join(
            sentences[:sentence_count]
        )


# ============================================================
# NORMAL CONVERSATION
# ============================================================

def normal_conversation(question):

    q = question.lower().strip()

    if q in [
        "hello",
        "hi",
        "hey",
        "hello jarvis",
        "hi jarvis",
        "hey jarvis"
    ]:

        return (
            "Hello! I'm JARVIS. 🤖\n\n"
            "I'm ready to help you with "
            "your PDF document."
        )

    if (
        "who are you" in q
        or "what are you" in q
    ):

        return (
            "I'm JARVIS, an intelligent "
            "Python NLP chatbot with "
            "PDF document intelligence. 🤖"
        )

    if (
        "what can you do" in q
        or "what do you do" in q
    ):

        return (
            "I can read your PDF, search its "
            "contents, answer questions, "
            "generate summaries, and maintain "
            "conversation context."
        )

    if q in [
        "thanks",
        "thank you",
        "thanks jarvis",
        "thank you jarvis"
    ]:

        return "You're welcome! 🤖"

    if q in [
        "bye",
        "goodbye",
        "bye jarvis"
    ]:

        return (
            "Goodbye! I'll be here whenever "
            "you need me. 🤖"
        )

    return None


# ============================================================
# DETECT SUMMARY REQUEST
# ============================================================

def is_summary_request(question):

    q = question.lower().strip()

    phrases = [
        "summarize",
        "summarise",
        "summary",
        "main points",
        "key points",
        "important points",
        "summarize this pdf",
        "summarise this pdf",
        "summarize the pdf",
        "summarise the pdf",
        "summarize this document",
        "summarise this document",
        "summarize the document",
        "summarise the document",
        "explain this document",
        "explain the document",
        "give me a summary",
        "give me the summary"
    ]

    return any(
        phrase in q
        for phrase in phrases
    )


# ============================================================
# CONVERSATION MEMORY
# ============================================================

def get_conversation_context():

    if not st.session_state.messages:

        return ""

    recent_messages = (
        st.session_state.messages[-6:]
    )

    context_parts = []

    for message in recent_messages:

        role = message["role"]
        content = message["content"]

        context_parts.append(
            f"{role}: {content}"
        )

    return "\n".join(
        context_parts
    )


# ============================================================
# RESOLVE FOLLOW-UP QUESTIONS
# ============================================================

def resolve_question(question):

    q = question.strip()

    if not st.session_state.messages:

        return q

    q_lower = q.lower()

    follow_up_words = [
        "it",
        "its",
        "they",
        "them",
        "their",
        "this",
        "that",
        "these",
        "those",
        "its types",
        "what about it",
        "tell me more",
        "explain more",
        "why",
        "how"
    ]

    is_follow_up = any(
        phrase in q_lower
        for phrase in follow_up_words
    )

    if not is_follow_up:

        return q

    # Find the latest meaningful user question
    previous_user_questions = []

    for message in st.session_state.messages:

        if message["role"] == "user":

            previous_user_questions.append(
                message["content"]
            )

    if not previous_user_questions:

        return q

    previous_question = (
        previous_user_questions[-1]
    )

    # Add previous question as context
    return (
        f"{previous_question}. "
        f"Follow-up question: {q}"
    )


# ============================================================
# GENERATE PDF ANSWER
# ============================================================

def generate_pdf_answer(
    question,
    results
):

    if not results:

        return (
            "I couldn't find relevant information "
            "in the uploaded PDF.\n\n"
            "Try asking the question using "
            "different words."
        )

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question.lower()
        )
    )

    candidates = []

    for result in results:

        sentences = split_sentences(
            result["text"]
        )

        for sentence in sentences:

            sentence_words = set(
                re.findall(
                    r"\b[a-zA-Z]{3,}\b",
                    sentence.lower()
                )
            )

            overlap = len(
                question_words.intersection(
                    sentence_words
                )
            )

            candidates.append(
                (
                    overlap,
                    result["score"],
                    sentence
                )
            )

    candidates.sort(
        key=lambda x: (
            x[0],
            x[1]
        ),
        reverse=True
    )

    selected = []

    for _, _, sentence in candidates:

        if sentence not in selected:

            selected.append(sentence)

        if len(selected) >= 5:
            break

    if not selected:

        return (
            "I couldn't find a suitable answer "
            "in the uploaded document."
        )

    answer = " ".join(selected)

    if len(answer) > 1800:

        answer = answer[:1800]

        last_space = answer.rfind(" ")

        if last_space > 0:

            answer = answer[
                :last_space
            ]

        answer += "..."

    return answer


# ============================================================
# MAIN ANSWER FUNCTION
# ============================================================

def generate_answer(question):

    # Normal conversation
    conversational_answer = (
        normal_conversation(question)
    )

    if conversational_answer:

        return conversational_answer

    # Check PDF
    if not st.session_state.pdf_name:

        return (
            "Please upload a PDF first. 📄\n\n"
            "Then I can answer questions "
            "or summarize the document."
        )

    # Summary
    if is_summary_request(question):

        with st.spinner(
            "JARVIS is creating a summary..."
        ):

            summary = summarize_document(
                st.session_state.pdf_text,
                sentence_count=7
            )

        return (
            "### 📄 Document Summary\n\n"
            + summary
        )

    # Resolve follow-up question
    search_question = resolve_question(
        question
    )

    # Search PDF
    results = search_document(
        search_question,
        top_k=5
    )

    return generate_pdf_answer(
        search_question,
        results
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 JARVIS")

    st.caption(
        "Python NLP PDF Assistant"
    )

    st.divider()

    st.subheader("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help=(
            "Upload a PDF and ask JARVIS "
            "questions about it."
        )
    )

    # --------------------------------------------------------
    # PROCESS PDF
    # --------------------------------------------------------

    if uploaded_file is not None:

        if (
            st.session_state.pdf_name
            != uploaded_file.name
        ):

            with st.spinner(
                "JARVIS is reading your PDF..."
            ):

                pdf_text, page_count = (
                    extract_pdf_text(
                        uploaded_file
                    )
                )

                if pdf_text:

                    chunks = create_chunks(
                        pdf_text
                    )

                    vectorizer, matrix = (
                        build_search_engine(
                            chunks
                        )
                    )

                    if vectorizer is not None:

                        st.session_state.pdf_text = (
                            pdf_text
                        )

                        st.session_state.chunks = (
                            chunks
                        )

                        st.session_state.vectorizer = (
                            vectorizer
                        )

                        st.session_state.matrix = (
                            matrix
                        )

                        st.session_state.pdf_name = (
                            uploaded_file.name
                        )

                        st.session_state.page_count = (
                            page_count
                        )

                        st.session_state.messages = []

                        st.success(
                            "PDF loaded successfully!"
                        )

                    else:

                        st.error(
                            "Could not process the PDF."
                        )

                else:

                    st.error(
                        "No readable text was found "
                        "in this PDF."
                    )

    # --------------------------------------------------------
    # DOCUMENT STATUS
    # --------------------------------------------------------

    st.divider()

    st.subheader("📊 Document Status")

    if st.session_state.pdf_name:

        st.write(
            f"**File:** "
            f"{st.session_state.pdf_name}"
        )

        st.write(
            f"**Pages:** "
            f"{st.session_state.page_count}"
        )

        st.write(
            f"**Chunks:** "
            f"{len(st.session_state.chunks)}"
        )

        st.success(
            "Document ready"
        )

    else:

        st.info(
            "No PDF uploaded."
        )

    # --------------------------------------------------------
    # CLEAR CONVERSATION
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

st.subheader("📊 JARVIS Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "NLP Engine",
        "ACTIVE"
    )

with col2:

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

with col3:

    st.metric(
        "Document Chunks",
        len(st.session_state.chunks)
    )

with col4:

    st.metric(
        "Document",
        (
            "READY"
            if st.session_state.pdf_name
            else "NONE"
        )
    )


# ============================================================
# CHAT
# ============================================================

st.divider()

st.subheader("💬 Chat with JARVIS")


# ============================================================
# WELCOME MESSAGE
# ============================================================

if not st.session_state.messages:

    with st.chat_message("assistant"):

        st.markdown(
            """
            **Hello! I'm JARVIS. 🤖**

            Upload a PDF using the sidebar.

            You can ask me:

            - What is this document about?
            - What is Machine Learning?
            - Explain Natural Language Processing.
            - What are the main points?
            - Summarize this PDF.

            You can also ask follow-up questions
            using words like **it**, **its**, or
            **they**.
            """
        )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask JARVIS something..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Show user question
    with st.chat_message("user"):

        st.markdown(question)

    # Generate response
    with st.chat_message("assistant"):

        answer = generate_answer(
            question
        )

        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )