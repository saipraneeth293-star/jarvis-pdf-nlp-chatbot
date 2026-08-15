from pathlib import Path

from chatbot import JARVIS


jarvis = JARVIS()


print("=" * 60)
print("                 JARVIS")
print("          Intelligent AI Assistant")
print("=" * 60)


pdf_path = input(
    "\nEnter PDF path "
    "(or press Enter to skip): "
).strip()


if pdf_path:

    try:

        info = jarvis.load_document(
            Path(pdf_path)
        )

        print("\n📄 Document loaded successfully!")

        print(
            "File:",
            info["filename"]
        )

        print(
            "Pages:",
            info["pages"]
        )

        print(
            "Sections:",
            info["chunks"]
        )

    except Exception as error:

        print(
            "\n❌ Could not load PDF:"
        )

        print(error)


print("\nJARVIS is ready.")
print("Type 'exit' to quit.")


while True:

    user_input = input("\nYou: ")

    if user_input.lower() in [
        "exit",
        "quit"
    ]:

        print(
            "JARVIS: Goodbye! 👋"
        )

        break

    try:

        response = jarvis.respond(
            user_input
        )

        print(
            "\nJARVIS:",
            response
        )

    except Exception as error:

        print(
            "\nJARVIS encountered an error:"
        )

        print(error)