
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


class AnswerEngine:

    def __init__(self):

        print("Loading JARVIS answer engine...")

        model_name = "google/flan-t5-small"

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model.to(self.device)

        print(
            f"Answer engine ready ({self.device})."
        )

    def generate(self, question, context):

        prompt = f"""
Answer the question using ONLY the context below.

If the context does not contain the answer,
say that the information could not be found
in the document.

Give a short, clear and natural answer.

Context:
{context}

Question:
{question}

Answer:
"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False
            )

        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return answer.strip()