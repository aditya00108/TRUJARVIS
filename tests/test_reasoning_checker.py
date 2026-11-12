
"""
TRUJARVIS - Reasoning Checker Tests
"""

from core.quality.reasoning_checker import ReasoningChecker


def run_tests():

    print("\n===== REASONING CHECKER TESTS =====")

    nums = [2, 3, 4, 10, 40]
    target = 10

    # Test 1: Correct Binary Search trace
    correct_trace = [
        {"left": 0, "right": 4, "mid": 2, "value": 4},
        {"left": 3, "right": 4, "mid": 3, "value": 10},
    ]

    result = ReasoningChecker.validate_binary_search_trace(
        nums, target, correct_trace, reported_index=3
    )

    assert result["valid"] is True, result
    assert result["actual_index"] == 3
    print("[PASS] Correct Binary Search trace")

    # Test 2: Incorrect array value
    wrong_value_trace = [
        {"left": 0, "right": 4, "mid": 2, "value": 10},
    ]

    result = ReasoningChecker.validate_binary_search_trace(
        nums, target, wrong_value_trace
    )

    assert result["valid"] is False
    print("[PASS] Incorrect array value detection")

    # Test 3: Incorrect mid calculation
    wrong_mid_trace = [
        {"left": 0, "right": 4, "mid": 3},
    ]

    result = ReasoningChecker.validate_binary_search_trace(
        nums, target, wrong_mid_trace
    )

    assert result["valid"] is False
    print("[PASS] Incorrect mid detection")

    # Test 4: Incorrect boundary update
    wrong_boundary_trace = [
        {"left": 0, "right": 4, "mid": 2},
        {"left": 2, "right": 4, "mid": 3},
    ]

    result = ReasoningChecker.validate_binary_search_trace(
        nums, target, wrong_boundary_trace
    )

    assert result["valid"] is False
    print("[PASS] Incorrect boundary detection")

    # Test 5: Unsorted array
    result = ReasoningChecker.validate_binary_search_trace(
        [10, 2, 4, 3, 40],
        target,
        correct_trace,
    )

    assert result["valid"] is False
    print("[PASS] Unsorted array detection")

    # Test 6: Incorrect reported index
    result = ReasoningChecker.validate_binary_search_trace(
        nums,
        target,
        correct_trace,
        reported_index=2,
    )

    assert result["valid"] is False
    print("[PASS] Incorrect final index detection")

    # Test 7: Empty trace
    result = ReasoningChecker.validate_binary_search_trace(
        nums, target, []
    )

    assert result["valid"] is False
    print("[PASS] Empty trace detection")

    print("\n===== ALL REASONING CHECKER TESTS PASSED =====")


if __name__ == "__main__":
    run_tests()
