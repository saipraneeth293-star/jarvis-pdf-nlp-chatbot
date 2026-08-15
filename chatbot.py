import re
import random
import math
from datetime import datetime
from pathlib import Path

import nltk
from nltk.tokenize import RegexpTokenizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pypdf import PdfReader


class JARVIS:

    def __init__(self):

        self.name = "JARVIS"

        self.document_text = ""
        self.document_name = None
        self.document_pages = 0

        self.tokenizer = RegexpTokenizer(r"\w+")

        # =====================================================
        # TRAINING DATA
        # =====================================================

        self.intent_data = {

            "greeting": [
                "hello",
                "hi",
                "hey",
                "hello jarvis",
                "hi jarvis",
                "good morning",
                "good evening",
                "good afternoon",
                "hey there",
            ],

            "goodbye": [
                "bye",
                "goodbye",
                "see you",
                "see you later",
                "exit",
                "quit",
            ],

            "identity": [
                "who are you",
                "what is your name",
                "tell me your name",
                "who created you",
                "what are you",
            ],

            "capabilities": [
                "what can you do",
                "what are your capabilities",
                "how can you help me",
                "what tasks can you perform",
                "help me",
                "what can jarvis do",
            ],

            "time": [
                "what time is it",
                "tell me the time",
                "current time",
                "time now",
                "what is the current time",
            ],

            "date": [
                "what is today's date",
                "what date is today",
                "current date",
                "today's date",
                "tell me today's date",
            ],

            "ai": [
                "what is artificial intelligence",
                "explain artificial intelligence",
                "what is ai",
                "tell me about artificial intelligence",
                "define artificial intelligence",
            ],

            "machine_learning": [
                "what is machine learning",
                "explain machine learning",
                "what is ml",
                "tell me about machine learning",
                "define machine learning",
            ],

            "nlp": [
                "what is natural language processing",
                "what is nlp",
                "explain nlp",
                "tell me about natural language processing",
                "define natural language processing",
            ],

            "python": [
                "what is python",
                "tell me about python",
                "why is python popular",
                "what can python do",
            ],

            "calculator": [
                "calculate 10 plus 20",
                "calculate 50 minus 10",
                "calculate 5 multiplied by 10",
                "calculate 100 divided by 5",
                "what is 25 plus 25",
                "what is 100 minus 50",
                "what is 10 times 5",
                "what is 100 divided by 10",
            ],

            "thanks": [
                "thank you",
                "thanks",
                "thank you jarvis",
                "thanks jarvis",
            ],
        }


        # =====================================================
        # PREPARE NLP TRAINING DATA
        # =====================================================

        self.training_sentences = []
        self.training_labels = []

        for intent, sentences in self.intent_data.items():

            for sentence in sentences:

                self.training_sentences.append(
                    self.preprocess(sentence)
                )

                self.training_labels.append(intent)


        # =====================================================
        # TF-IDF NLP MODEL
        # =====================================================

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True
        )

        self.training_vectors = (
            self.vectorizer.fit_transform(
                self.training_sentences
            )
        )


        print("JARVIS NLP engine initialized successfully.")


    # =========================================================
    # NLP PREPROCESSING
    # =========================================================

    def preprocess(self, text):

        tokens = self.tokenizer.tokenize(
            text.lower()
        )

        return " ".join(tokens)


    # =========================================================
    # INTENT DETECTION
    # =========================================================

    def detect_intent(self, text):

        processed = self.preprocess(text)

        query_vector = self.vectorizer.transform(
            [processed]
        )

        similarities = cosine_similarity(
            query_vector,
            self.training_vectors
        )[0]

        best_index = similarities.argmax()

        confidence = float(
            similarities[best_index]
        )

        intent = self.training_labels[
            best_index
        ]

        # Minimum confidence threshold

        if confidence < 0.20:

            return "unknown", confidence

        return intent, confidence


    # =========================================================
    # MAIN RESPONSE
    # =========================================================

    def respond(self, user_input):

        if not user_input:
            return "Please enter a message."

        text = user_input.strip()

        # ---------------------------------------------
        # PDF QUESTION
        # ---------------------------------------------

        if self.document_text:

            pdf_keywords = [
                "document",
                "pdf",
                "file",
                "document says",
                "according to",
                "uploaded",
                "this file",
                "this document",
            ]

            if any(
                keyword in text.lower()
                for keyword in pdf_keywords
            ):

                return self.answer_document(
                    text
                )


        # ---------------------------------------------
        # CALCULATOR
        # ---------------------------------------------

        if self.looks_like_calculation(text):

            return self.calculate(text)


        # ---------------------------------------------
        # INTENT
        # ---------------------------------------------

        intent, confidence = self.detect_intent(
            text
        )


        # ---------------------------------------------
        # GREETING
        # ---------------------------------------------

        if intent == "greeting":

            return random.choice(
                [
                    "Hello! I'm JARVIS. How can I help you?",
                    "Hello! JARVIS is ready to assist you.",
                    "Hi! What can I do for you today?",
                ]
            )


        # ---------------------------------------------
        # GOODBYE
        # ---------------------------------------------

        if intent == "goodbye":

            return (
                "Goodbye! I'll be here whenever "
                "you need me."
            )


        # ---------------------------------------------
        # IDENTITY
        # ---------------------------------------------

        if intent == "identity":

            return (
                "I'm JARVIS, an intelligent "
                "Python-based conversational AI "
                "assistant built using NLP."
            )


        # ---------------------------------------------
        # CAPABILITIES
        # ---------------------------------------------

        if intent == "capabilities":

            return (
                "I can help you with:\n\n"
                "• Natural-language conversations\n"
                "• Intent detection\n"
                "• Mathematical calculations\n"
                "• Date and time\n"
                "• AI and machine-learning questions\n"
                "• NLP questions\n"
                "• Python questions\n"
                "• PDF/document analysis\n"
                "• General task assistance"
            )


        # ---------------------------------------------
        # TIME
        # ---------------------------------------------

        if intent == "time":

            current_time = datetime.now()

            return (
                "The current time is "
                + current_time.strftime("%I:%M %p")
                + "."
            )


        # ---------------------------------------------
        # DATE
        # ---------------------------------------------

        if intent == "date":

            current_date = datetime.now()

            return (
                "Today's date is "
                + current_date.strftime(
                    "%d %B %Y"
                )
                + "."
            )


        # ---------------------------------------------
        # AI
        # ---------------------------------------------

        if intent == "ai":

            return (
                "Artificial Intelligence (AI) is "
                "the field of computer science that "
                "focuses on creating systems capable "
                "of performing tasks that normally "
                "require human intelligence, such as "
                "learning, reasoning, prediction and "
                "language understanding."
            )


        # ---------------------------------------------
        # MACHINE LEARNING
        # ---------------------------------------------

        if intent == "machine_learning":

            return (
                "Machine Learning is a branch of AI "
                "where computers learn patterns from "
                "data and use those patterns to make "
                "predictions or decisions."
            )


        # ---------------------------------------------
        # NLP
        # ---------------------------------------------

        if intent == "nlp":

            return (
                "Natural Language Processing, or NLP, "
                "is a branch of AI that enables computers "
                "to process, understand and work with "
                "human language."
            )


        # ---------------------------------------------
        # PYTHON
        # ---------------------------------------------

        if intent == "python":

            return (
                "Python is a high-level programming "
                "language known for its simple syntax "
                "and extensive ecosystem. It is widely "
                "used in AI, machine learning, data "
                "science, automation and web development."
            )


        # ---------------------------------------------
        # THANKS
        # ---------------------------------------------

        if intent == "thanks":

            return random.choice(
                [
                    "You're welcome!",
                    "Happy to help!",
                    "Anytime!",
                ]
            )


        # ---------------------------------------------
        # UNKNOWN
        # ---------------------------------------------

        return (
            "I'm still learning. I couldn't "
            "fully understand that question. "
            "Try asking me in another way."
        )


    # =========================================================
    # CALCULATOR DETECTION
    # =========================================================

    def looks_like_calculation(self, text):

        lower = text.lower()

        if any(
            phrase in lower
            for phrase in [
                "calculate",
                "plus",
                "minus",
                "multiplied by",
                "divided by",
                "times",
            ]
        ):

            return True


        # Mathematical symbols + numbers

        if (
            any(
                symbol in text
                for symbol in [
                    "+",
                    "*",
                    "/",
                    "%"
                ]
            )
            and
            any(
                char.isdigit()
                for char in text
            )
        ):

            return True


        return False


    # =========================================================
    # CALCULATOR
    # =========================================================

    def calculate(self, text):

        expression = text.lower()

        replacements = {
            "calculate": "",
            "what is": "",
            "plus": "+",
            "minus": "-",
            "multiplied by": "*",
            "times": "*",
            "divided by": "/",
        }

        for old, new in replacements.items():

            expression = expression.replace(
                old,
                new
            )


        expression = expression.strip()


        # Keep only safe mathematical characters

        if not re.fullmatch(
            r"[0-9+\-*/().%\s]+",
            expression
        ):

            return (
                "I couldn't identify a valid "
                "mathematical expression."
            )


        try:

            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
                {}
            )

            return (
                f"🧮 The answer is **{result}**."
            )

        except Exception:

            return (
                "I couldn't calculate that. "
                "Please check your expression."
            )


    # =========================================================
    # PDF LOADING
    # =========================================================

    def load_document(self, pdf_path):

        pdf_path = Path(pdf_path)

        reader = PdfReader(
            str(pdf_path)
        )

        text = ""

        for page in reader.pages:

            try:

                page_text = (
                    page.extract_text()
                )

                if page_text:

                    text += (
                        page_text + "\n"
                    )

            except Exception:

                continue


        self.document_text = text
        self.document_name = pdf_path.name
        self.document_pages = len(
            reader.pages
        )


        return {
            "filename": pdf_path.name,
            "pages": len(reader.pages),
            "characters": len(text),
            "chunks": max(
                1,
                len(text) // 1000
            )
        }


    # =========================================================
    # PDF QUESTION ANSWERING
    # =========================================================

    def answer_document(self, question):

        if not self.document_text:

            return (
                "No PDF is currently loaded."
            )


        # Remove common question words

        stop_words = {
            "what",
            "when",
            "where",
            "which",
            "who",
            "how",
            "why",
            "is",
            "are",
            "the",
            "a",
            "an",
            "of",
            "in",
            "on",
            "to",
            "this",
            "document",
            "pdf",
            "file",
            "tell",
            "me",
        }


        question_words = set(
            self.tokenizer.tokenize(
                question.lower()
            )
        )

        question_words -= stop_words


        # Split document into sentences

        sentences = re.split(
            r"(?<=[.!?])\s+",
            self.document_text
        )


        scored_sentences = []


        for sentence in sentences:

            sentence_lower = (
                sentence.lower()
            )

            score = 0

            for word in question_words:

                if word in sentence_lower:

                    score += 1


            if score > 0:

                scored_sentences.append(
                    (
                        score,
                        sentence.strip()
                    )
                )


        scored_sentences.sort(
            key=lambda item: item[0],
            reverse=True
        )


        if not scored_sentences:

            return (
                "I couldn't find a relevant "
                "answer in the uploaded PDF."
            )


        best_sentences = [
            sentence
            for score, sentence
            in scored_sentences[:5]
        ]


        answer = " ".join(
            best_sentences
        )


        return (
            "📄 **Based on your document:**\n\n"
            + answer[:3000]
        )