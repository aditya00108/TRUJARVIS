
"""
TRUJARVIS - LLM Quality Integration Test
"""

from core.llm_engine import LLMEngine


def run_test():

    print("\n===== LLM QUALITY INTEGRATION TEST =====")

    engine = LLMEngine()

    messages = [
        {
            "role": "user",
            "content": (
                "Write a short valid Python function "
                "that adds two numbers. Return Python code."
            ),
        }
    ]

    # Generate complete response
    response = "".join(
        engine.generate_response(
            messages=messages,
            num_predict=256,
        )
    )

    assert response.strip(), "Empty AI response"

    print("\n[PASS] AI response generated")

    # Retrieve quality report
    report = engine.last_quality_report

    assert isinstance(report, dict), "Quality report missing"

    assert report["response_validation"] is not None

    assert isinstance(report["code_validation"], list)

    print("[PASS] Quality report generated")

    print("\nResponse:")
    print(response)

    print("\nQuality Report:")
    print(report)

    print("\n===== INTEGRATION TEST COMPLETED =====")


if __name__ == "__main__":
    run_test()
