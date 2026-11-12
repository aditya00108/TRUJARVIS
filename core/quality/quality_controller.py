
"""
TRUJARVIS - Quality Controller

Coordinates response, code and reasoning
validation modules.
"""

from core.quality.response_validator import ResponseValidator
from core.quality.code_validator import CodeValidator
from core.quality.reasoning_checker import ReasoningChecker


class QualityController:
    """Central controller for response quality checks."""

    def validate_response(
        self,
        response: str,
        reasoning_data=None,
    ):

        report = {
            "valid": True,
            "response_validation": None,
            "code_validation": [],
            "reasoning_validation": None,
            "errors": [],
            "warnings": [],
        }

        # 1. Basic response validation
        response_result = ResponseValidator.validate(response)

        report["response_validation"] = response_result
        report["errors"].extend(response_result["errors"])
        report["warnings"].extend(response_result["warnings"])

        # 2. Stop if response is structurally invalid
        if not response_result["valid"]:
            report["valid"] = False
            return report

        # 3. Validate supported code blocks
        code_results = CodeValidator.validate_response(response)

        report["code_validation"] = code_results

        for result in code_results:
            if not result["valid"]:
                report["errors"].append(
                    f"{result['language']} code validation failed: "
                    f"{result['error']}"
                )

        # 4. Validate structured reasoning when provided
        if reasoning_data is not None:

            if not isinstance(reasoning_data, dict):
                report["errors"].append(
                    "Reasoning data must be a dictionary."
                )

            else:
                try:
                    reasoning_result = (
                        ReasoningChecker.validate_binary_search_trace(
                            nums=reasoning_data["nums"],
                            target=reasoning_data["target"],
                            steps=reasoning_data["steps"],
                            reported_index=reasoning_data.get(
                                "reported_index"
                            ),
                        )
                    )

                    report["reasoning_validation"] = reasoning_result

                    report["errors"].extend(
                        reasoning_result["errors"]
                    )

                    report["warnings"].extend(
                        reasoning_result["warnings"]
                    )

                except KeyError as error:
                    report["errors"].append(
                        f"Missing reasoning field: {error}"
                    )

        report["valid"] = len(report["errors"]) == 0

        return report
