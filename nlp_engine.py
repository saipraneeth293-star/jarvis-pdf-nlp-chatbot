import joblib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"


VECTOR_FILE = (
    MODEL_DIR /
    "tfidf_vectorizer.pkl"
)

MODEL_FILE = (
    MODEL_DIR /
    "intent_model.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

vectorizer = None
model = None


try:

    vectorizer = joblib.load(
        VECTOR_FILE
    )

    model = joblib.load(
        MODEL_FILE
    )

    print("NLP model loaded successfully.")


except Exception as error:

    print(
        "Warning: NLP model could not be loaded."
    )

    print(error)


# ============================================================
# INTENT PREDICTION
# ============================================================

def predict_intent(text):

    """
    Predict the user's intent using
    the TF-IDF + classification model.
    """

    if not text:

        return "unknown", 0.0


    # --------------------------------------------------------
    # If ML model exists
    # --------------------------------------------------------

    if (
        vectorizer is not None
        and
        model is not None
    ):

        try:

            X = vectorizer.transform(
                [text]
            )

            prediction = model.predict(
                X
            )[0]


            confidence = 0.0


            if hasattr(
                model,
                "decision_function"
            ):

                scores = (
                    model.decision_function(
                        X
                    )
                )

                if hasattr(
                    scores,
                    "__len__"
                ):

                    try:

                        import numpy as np

                        scores = np.asarray(
                            scores
                        )

                        confidence = float(
                            np.max(
                                scores
                            )
                        )

                    except Exception:

                        confidence = 0.0


            return (
                str(prediction),
                confidence
            )


        except Exception:

            pass


    # --------------------------------------------------------
    # Fallback NLP rules
    # --------------------------------------------------------

    text_lower = text.lower()


    if any(
        word in text_lower
        for word in [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good evening"
        ]
    ):

        return "greeting", 1.0


    if any(
        word in text_lower
        for word in [
            "bye",
            "goodbye",
            "see you",
            "exit"
        ]
    ):

        return "goodbye", 1.0


    if (
        "your name" in text_lower
        or
        "who are you" in text_lower
    ):

        return "name", 1.0


    if any(
        phrase in text_lower
        for phrase in [
            "what can you do",
            "help me",
            "your capabilities"
        ]
    ):

        return "capabilities", 1.0


    if (
        "time" in text_lower
        and
        any(
            word in text_lower
            for word in [
                "what",
                "current",
                "tell"
            ]
        )
    ):

        return "time", 1.0


    if (
        "date" in text_lower
        and
        any(
            word in text_lower
            for word in [
                "what",
                "today",
                "current"
            ]
        )
    ):

        return "date", 1.0


    # Mathematical expression

    mathematical_symbols = (
        "+",
        "-",
        "*",
        "/",
        "%"
    )


    if any(
        symbol in text_lower
        for symbol in mathematical_symbols
    ):

        return "calculator", 1.0


    if any(
        phrase in text_lower
        for phrase in [
            "calculate",
            "how much is",
            "what is"
        ]
    ):

        # Don't classify every "what is" as math,
        # unless numbers are present.

        if any(
            char.isdigit()
            for char in text_lower
        ):

            return "calculator", 1.0


    return "unknown", 0.0