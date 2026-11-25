
from core.llm_engine import LLMEngine


def run_test():
    print("\n===== RETRY LIMIT TEST =====")

    engine = LLMEngine()
    call_count = {"value": 0}

    def fake_generation(messages, model, options):
        call_count["value"] += 1
        return "```python\ndef broken(:\n    pass\n```"

    engine._generate_complete_response = fake_generation

    result = list(
        engine.generate_response(
            messages=[
                {
                    "role": "user",
                    "content": "Write a Python function."
                }
            ]
        )
    )

    assert call_count["value"] == 3
    assert len(engine.attempt_reports) == 3
    assert engine.last_quality_report["valid"] is False
    assert len(result) == 1

    print("[PASS] Initial generation completed")
    print("[PASS] Two retries completed")
    print("[PASS] Maximum attempt limit enforced")
    print("[PASS] Final invalid report preserved")
    print("[PASS] Total attempts:", call_count["value"])

    print("\n===== RETRY LIMIT TEST PASSED =====")


if __name__ == "__main__":
    run_test()
