
"""
TRUJARVIS - Response Validator Tests
"""

from core.quality.response_validator import ResponseValidator


def run_tests():

    print("\n===== RESPONSE VALIDATOR TESTS =====")

    # Test 1: Valid response
    result = ResponseValidator.validate(
        "Binary Search is an efficient searching algorithm."
    )

    assert result["valid"] is True
    assert len(result["errors"]) == 0
    print("[PASS] Valid response")

    # Test 2: Empty response
    result = ResponseValidator.validate("")

    assert result["valid"] is False
    assert "Response is empty." in result["errors"]
    print("[PASS] Empty response detection")

    # Test 3: Whitespace response
    result = ResponseValidator.validate("   ")

    assert result["valid"] is False
    print("[PASS] Whitespace response detection")

    # Test 4: Non-string response
    result = ResponseValidator.validate(None)

    assert result["valid"] is False
    print("[PASS] Non-string response detection")

    # Test 5: Incomplete code fence
    result = ResponseValidator.validate(
        "Here is the code:\n```python\nprint('Hello')"
    )

    assert result["valid"] is True
    assert len(result["warnings"]) > 0
    print("[PASS] Incomplete code fence detection")

    # Test 6: Truncation marker
    result = ResponseValidator.validate(
        "This is an incomplete answer. [TRUNCATED]"
    )

    assert result["valid"] is True
    assert len(result["warnings"]) > 0
    print("[PASS] Truncation marker detection")

    print("\n===== ALL RESPONSE VALIDATOR TESTS PASSED =====")


if __name__ == "__main__":
    run_tests()
