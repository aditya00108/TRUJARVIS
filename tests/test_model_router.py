
"""
TRUJARVIS - Model Router Tests
"""

from core.model_router import ModelRouter
from providers.ollama_provider import OllamaProvider


def main():

    print("\n===== TRUJARVIS MODEL ROUTER TEST =====")

    router = ModelRouter()

    # TEST 1: Register provider
    print("\n[TEST 1] Registering Ollama provider...")

    provider = OllamaProvider()

    router.register_provider(
        name="ollama",
        provider=provider,
        make_default=True,
    )

    print("Registered providers:", list(router.providers.keys()))
    print("Default provider:", router.default_provider)

    # TEST 2: Connection
    print("\n[TEST 2] Checking provider connection...")

    connected, message = router.check_connection()

    print("Connection:", connected)
    print("Message:", message)

    if not connected:
        print("Ollama unavailable. Stopping tests.")
        return

    # TEST 3: Model discovery
    print("\n[TEST 3] Discovering models...")

    models = router.list_models()

    for model in models:
        print("-", model)

    model_name = "llama3.2:latest"

    if model_name not in models:
        print("Required model not found.")
        return

    # TEST 4: Generate response through router
    print("\n[TEST 4] Testing router response...")

    messages = [
        {
            "role": "user",
            "content": "What is artificial intelligence? Explain briefly."
        }
    ]

    options = {
        "temperature": 0.7,
        "num_ctx": 2048,
        "num_predict": 128,
    }

    try:
        print("\nTRUJARVIS: ", end="", flush=True)

        for chunk in router.generate_response(
            messages=messages,
            model=model_name,
            options=options,
        ):
            print(chunk, end="", flush=True)

        print("\n\nRouter response test passed!")

    except Exception as error:
        print("\nRouter test failed:", error)
        return

    print("\n===== ALL ROUTER TESTS COMPLETED =====")


if __name__ == "__main__":
    main()
