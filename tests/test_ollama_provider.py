
"""
TRUJARVIS - Ollama Provider Tests

Tests connection, model discovery and streaming.
"""

from providers.ollama_provider import OllamaProvider


def main():

    print("\n===== TRUJARVIS OLLAMA PROVIDER TEST =====")

    provider = OllamaProvider()

    # TEST 1: Connection
    print("\n[TEST 1] Checking Ollama connection...")

    connected, message = provider.check_connection()

    print("Connection:", connected)
    print("Message:", message)

    if not connected:
        print("Ollama is unavailable. Start Ollama and retry.")
        return

    # TEST 2: Model discovery
    print("\n[TEST 2] Fetching available models...")

    try:
        models = provider.list_models()

        for model in models:
            print("-", model)

    except Exception as error:
        print("Model discovery failed:", error)
        return

    model_name = "llama3.2:latest"

    if model_name not in models:
        print(f"\nRequired model not found: {model_name}")
        print("Available models:", models)
        return

    # TEST 3: Streaming response
    print("\n[TEST 3] Testing streaming response...")

    messages = [
        {
            "role": "user",
            "content": "Explain Python in exactly two short sentences."
        }
    ]

    options = {
        "temperature": 0.7,
        "num_ctx": 2048,
        "num_predict": 128,
    }

    try:
        print("\nTRUJARVIS: ", end="", flush=True)

        for chunk in provider.stream_chat(
            model=model_name,
            messages=messages,
            options=options,
        ):
            print(chunk, end="", flush=True)

        print("\n\nStreaming test passed!")

    except Exception as error:
        print("\nStreaming test failed:", error)
        return

    print("\n===== ALL TESTS COMPLETED =====")


if __name__ == "__main__":
    main()
