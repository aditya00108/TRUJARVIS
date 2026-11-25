
from core.llm_engine import LLMEngine


def run_test():
    print("\n===== SELF-CORRECTION TEST =====")

    engine = LLMEngine()

    responses = [
        "```python\ndef add(a, b):\n    return a +\n```",
        "```python\ndef add(a, b):\n    return a + b\n```",
    ]

    call_count = {"value": 0}

    def fake_generation(messages, model, options):
        response = responses[call_count["value"]]
        call_count["value"] += 1
        return response

    engine._generate_complete_response = fake_generation

    result = list(
        engine.generate_response(
            messages=[
                {
                    "role": "user",
                    "content": "Write a Python function to add two numbers."
                }
            ]
        )
    )

    assert call_count["value"] == 2, "Expected exactly two generation attempts."
    assert len(engine.attempt_reports) == 2, "Expected two validation reports."
    assert engine.attempt_reports[0]["valid"] is False
    assert engine.attempt_reports[1]["valid"] is True
    assert engine.last_quality_report["valid"] is True
    assert "return a + b" in result[0]

    print("[PASS] Invalid response detected")
    print("[PASS] Correction attempt triggered")
    print("[PASS] Corrected response validated")
    print("[PASS] Total attempts:", call_count["value"])

    print("\n===== SELF-CORRECTION TEST PASSED =====")


if __name__ == "__main__":
    run_test()
