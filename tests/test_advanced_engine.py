
from core.llm_engine import LLMEngine


def main():

    print("TRUJARVIS Advanced Engine Test")

    engine = LLMEngine()

    connected, message = engine.check_connection()

    print("\nConnection:", connected)
    print(message)

    if not connected:
        return

    print("\nAvailable Models:")

    for model in engine.get_available_models():
        print("-", model)

    messages = [
        {
            "role": "user",
            "content": "Explain Python in three sentences."
        }
    ]

    print("\nAI Response:\n")

    for token in engine.generate_response(
        messages,
        temperature=0.5,
        top_p=0.9,
        num_ctx=2048,
        num_predict=256,
    ):

        print(token, end="", flush=True)

    print("\n\nAdvanced Engine Test Completed!")


if __name__ == "__main__":
    main()
