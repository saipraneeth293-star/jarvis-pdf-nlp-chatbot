from pathlib import Path

from document_engine import DocumentEngine


engine = DocumentEngine()

pdf_path = Path(
    input("Enter PDF path: ").strip()
)

info = engine.load_pdf(
    pdf_path
)

print("\n" + "=" * 60)
print("DOCUMENT LOADED")
print("=" * 60)

print("Filename:", info["filename"])
print("Pages:", info["pages"])
print("Chunks:", info["chunks"])
print("Characters:", info["characters"])

print("\nAsk a question.")

while True:

    question = input("\nQuestion: ")

    if question.lower() in [
        "exit",
        "quit"
    ]:
        break

    results = engine.search(
        question,
        top_k=3
    )

    for result in results:

        print("\nSimilarity:",
              round(
                  result["similarity"],
                  3
              ))

        print(result["text"][:1000])

        print("-" * 60)