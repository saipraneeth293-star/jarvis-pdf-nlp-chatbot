import re


class QueryRouter:

    def __init__(self):
        self.document_keywords = [
            "pdf",
            "document",
            "file",
            "report",
            "according to",
            "in the document",
            "in this report",
            "this pdf",
            "chapter",
            "section",
            "page",
            "according to the report"
        ]

        self.calculation_patterns = [
            r"\d+\s*[\+\-\*\/xX]\s*\d+",
            r"\d+\s*percent",
            r"\d+\s*%",
            r"calculate",
            r"solve",
            r"what is \d+",
        ]

    def route(self, query, pdf_loaded=False):

        text = query.lower().strip()

        # -------------------------
        # CALCULATOR
        # -------------------------

        for pattern in self.calculation_patterns:

            if re.search(pattern, text):

                return "calculator"

        # -------------------------
        # DOCUMENT / PDF
        # -------------------------

        if pdf_loaded:

            for keyword in self.document_keywords:

                if keyword in text:

                    return "document"

            # If PDF is loaded and question
            # clearly refers to its contents

            document_question_words = [
                "what does",
                "what is the objective",
                "what are the results",
                "what methodology",
                "summarize",
                "summary",
                "explain the project",
                "find in the pdf",
                "tell me about the project"
            ]

            for phrase in document_question_words:

                if phrase in text:

                    return "document"

        # -------------------------
        # GENERAL CHAT
        # -------------------------

        return "general"