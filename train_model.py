import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


# ============================================================
# TRAINING DATA
# ============================================================

data = [

    # Greetings
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("good evening", "greeting"),
    ("hello jarvis", "greeting"),
    ("hi jarvis", "greeting"),

    # Goodbye
    ("bye", "goodbye"),
    ("goodbye", "goodbye"),
    ("see you later", "goodbye"),
    ("exit", "goodbye"),
    ("quit", "goodbye"),

    # Name
    ("what is your name", "name"),
    ("who are you", "name"),
    ("tell me your name", "name"),
    ("what should I call you", "name"),

    # Capabilities
    ("what can you do", "capabilities"),
    ("what are your capabilities", "capabilities"),
    ("how can you help me", "capabilities"),
    ("help me", "capabilities"),
    ("what tasks can you perform", "capabilities"),

    # Time
    ("what time is it", "time"),
    ("tell me the current time", "time"),
    ("what is the time now", "time"),
    ("current time", "time"),

    # Date
    ("what is today's date", "date"),
    ("what date is today", "date"),
    ("tell me today's date", "date"),
    ("current date", "date"),

    # Calculator
    ("calculate 10 plus 20", "calculator"),
    ("calculate 25 multiplied by 4", "calculator"),
    ("what is 50 divided by 5", "calculator"),
    ("what is 100 minus 25", "calculator"),
    ("calculate 10 percent of 500", "calculator"),
    ("25 + 50", "calculator"),
    ("100 / 5", "calculator"),
    ("20 * 10", "calculator"),

    # AI
    ("what is artificial intelligence", "knowledge"),
    ("explain artificial intelligence", "knowledge"),
    ("what is machine learning", "knowledge"),
    ("what is natural language processing", "knowledge"),
    ("what is nlp", "knowledge"),
    ("what is python", "knowledge"),

    # Identity
    ("who created you", "identity"),
    ("who made you", "identity"),
    ("who developed you", "identity"),

]


# ============================================================
# SEPARATE INPUT AND LABELS
# ============================================================

texts = [
    item[0]
    for item in data
]

labels = [
    item[1]
    for item in data
]


# ============================================================
# TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    sublinear_tf=True
)


X = vectorizer.fit_transform(
    texts
)


# ============================================================
# MODEL
# ============================================================

model = LinearSVC()

model.fit(
    X,
    labels
)


# ============================================================
# CREATE MODELS DIRECTORY
# ============================================================

os.makedirs(
    "models",
    exist_ok=True
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)

joblib.dump(
    model,
    "models/intent_model.pkl"
)


print()
print("=" * 55)
print("        JARVIS NLP MODEL TRAINED")
print("=" * 55)
print()
print("Training examples :", len(texts))
print("Intent categories  :", len(set(labels)))
print()
print("Created:")
print("models/tfidf_vectorizer.pkl")
print("models/intent_model.pkl")
print()
print("Training completed successfully!")