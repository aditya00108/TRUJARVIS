
"""
TRUJARVIS - Code Validator Tests
"""

from core.quality.code_validator import CodeValidator


def run_tests():

    print("\n===== CODE VALIDATOR TESTS =====")

    # Test 1: Extract code blocks
    response = """
    Here is Python code:

    ```python
    print("Hello World")
    ```
    """

    blocks = CodeValidator.extract_code_blocks(response)

    assert len(blocks) == 1
    assert blocks[0]["language"] == "python"

    print("[PASS] Code block extraction")

    # Test 2: Valid Python
    result = CodeValidator.validate_python(
        "def greet():\n    print('Hello')"
    )

    assert result["valid"] is True

    print("[PASS] Valid Python syntax")

    # Test 3: Invalid Python
    result = CodeValidator.validate_python(
        "def greet(\n    print('Hello')"
    )

    assert result["valid"] is False

    print("[PASS] Invalid Python detection")

    # Test 4: Valid C++
    cpp_code = """
    #include <iostream>
    using namespace std;

    int main() {
        cout << "Hello World";
        return 0;
    }
    """

    result = CodeValidator.validate_cpp(cpp_code)

    assert result["valid"] is True, result["error"]

    print("[PASS] Valid C++ syntax")

    # Test 5: Invalid C++
    cpp_code = """
    int main() {
        cout << "Hello"
        return 0;
    }
    """

    result = CodeValidator.validate_cpp(cpp_code)

    assert result["valid"] is False

    print("[PASS] Invalid C++ detection")

    # Test 6: Unsupported language
    result = CodeValidator.validate_code(
        "some code",
        "javascript"
    )

    assert result["valid"] is False

    print("[PASS] Unsupported language detection")

    # Test 7: Complete response validation
    response = """
    ```python
    print("TRUJARVIS")
    ```

    ```cpp
    int main() {
        return 0;
    }
    ```
    """

    results = CodeValidator.validate_response(response)

    assert len(results) == 2
    assert all(item["valid"] for item in results)

    print("[PASS] Complete response validation")

    print("\n===== ALL CODE VALIDATOR TESTS PASSED =====")


if __name__ == "__main__":
    run_tests()
