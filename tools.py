import re

from simpleeval import simple_eval


def calculate(expression):

    try:

        cleaned = re.sub(
            r"[^0-9+\-*/().% ]",
            "",
            expression
        )

        cleaned = cleaned.replace(
            "%",
            "/100"
        )

        result = simple_eval(cleaned)

        return str(result)

    except Exception:

        return None