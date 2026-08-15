import re
import numpy as np
from pathlib import Path
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


class DocumentEngine:

    def __init__(self):

        print("Loading document intelligence model...")

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.filename = None
        self.pages = 0
        self.text = ""
        self.chunks = []
        self.embeddings = None

        print("Document intelligence ready.")

    def load_pdf(self, filepath):

        filepath = Path(filepath)

        reader = PdfReader(filepath)

        self.filename = filepath.name
        self.pages = len(reader.pages)

        extracted_text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        self.text = self._clean_text(
            extracted_text
        )

        if not self.text:
            raise ValueError(
                "No readable text was found in this PDF."
            )

        self.chunks = self._create_chunks(
            self.text
        )

        self.embeddings = self.embedding_model.encode(
            self.chunks,
            normalize_embeddings=True
        )

        return {
            "filename": self.filename,
            "pages": self.pages,
            "chunks": len(self.chunks),
            "characters": len(self.text)
        }

    def _clean_text(self, text):

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _create_chunks(
        self,
        text,
        chunk_size=400,
        overlap=80
    ):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk = " ".join(
                words[start:end]
            )

            if chunk.strip():
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    def search(
        self,
        question,
        top_k=3
    ):

        if self.embeddings is None:

            return []

        question_embedding = (
            self.embedding_model.encode(
                [question],
                normalize_embeddings=True
            )[0]
        )

        similarities = np.dot(
            self.embeddings,
            question_embedding
        )

        indices = np.argsort(
            similarities
        )[::-1][:top_k]

        results = []

        for index in indices:

            results.append({
                "chunk_index": int(index),
                "text": self.chunks[index],
                "similarity": float(
                    similarities[index]
                )
            })

        return results

    def get_info(self):

        return {
            "filename": self.filename,
            "pages": self.pages,
            "chunks": len(self.chunks)
        }