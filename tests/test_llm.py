
from core.llm_engine import LLMEngine


def main():

    print("Initializing TRUJARVIS AI Engine...")

    engine = LLMEngine()

    connected, message = engine.check_connection()

    print("Connection status:", connected)
    print("Message:", message)

    if not connected:
        return

    print("\nTesting TRUJARVIS response:\n")

    messages = [
        {
            "role": "user",
            "content": "Introduce yourself as TRUJARVIS."
        }
    ]

    try:
        for token in engine.generate_response(messages):
            print(token, end="", flush=True)

        print("\n\nTest completed successfully!")

    except Exception as error:
        print("\nAI Engine Error:", error)


if __name__ == "__main__":
    main()
