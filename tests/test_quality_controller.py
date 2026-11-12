
"""
TRUJARVIS - Quality Controller Tests
"""

from core.quality.quality_controller import QualityController


def run_tests():

    print("\n===== QUALITY CONTROLLER TESTS =====")

    controller = QualityController()

    # Test 1: Valid response
    result = controller.validate_response(
        "Binary Search is an efficient algorithm."
    )

    assert result["valid"] is True, result
    print("[PASS] Basic response validation")

    # Test 2: Empty response
    result = controller.validate_response("")

    assert result["valid"] is False
    print("[PASS] Empty response rejection")

    # Test 3: Valid Python code
    response = """
    ```python
    def greet():
        print("Hello TRUJARVIS")
    ```
    """

    result = controller.validate_response(response)

    assert result["valid"] is True, result
    assert len(result["code_validation"]) == 1
    print("[PASS] Valid Python code validation")

    # Test 4: Invalid Python code
    response = """
    ```python
    def greet(
        print("Hello")
    ```
    """

    result = controller.validate_response(response)

    assert result["valid"] is False
    print("[PASS] Invalid Python code detection")

    # Test 5: Valid Binary Search reasoning
    reasoning_data = {
        "nums": [2, 3, 4, 10, 40],
        "target": 10,
        "steps": [
            {"left": 0, "right": 4, "mid": 2, "value": 4},
            {"left": 3, "right": 4, "mid": 3, "value": 10},
        ],
        "reported_index": 3,
    }

    result = controller.validate_response(
        "Target found at index 3.",
        reasoning_data=reasoning_data,
    )

    assert result["valid"] is True, result
    print("[PASS] Valid reasoning verification")

    # Test 6: Invalid Binary Search reasoning
    reasoning_data["reported_index"] = 2

    result = controller.validate_response(
        "Target found at index 2.",
        reasoning_data=reasoning_data,
    )

    assert result["valid"] is False
    print("[PASS] Invalid reasoning detection")

    # Test 7: Missing reasoning field
    result = controller.validate_response(
        "Test response.",
        reasoning_data={"nums": [1, 2, 3]},
    )

    assert result["valid"] is False
    print("[PASS] Missing reasoning field detection")

    print("\n===== ALL QUALITY CONTROLLER TESTS PASSED =====")


if __name__ == "__main__":
    run_tests()
