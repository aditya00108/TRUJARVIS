
"""
TRUJARVIS - Reasoning Checker

Performs deterministic verification of structured
algorithm traces, beginning with Binary Search.
"""


class ReasoningChecker:
    """Validates structured reasoning data."""

    @staticmethod
    def validate_binary_search_trace(
        nums: list,
        target: int,
        steps: list,
        reported_index=None,
    ) -> dict:
        """
        Verify a Binary Search dry run.

        Each step must contain:
        left, right, mid

        Optional:
        value: value reported at nums[mid]
        """

        errors = []
        warnings = []

        if not isinstance(nums, list) or not nums:
            return {
                "valid": False,
                "errors": ["Input array must be a non-empty list."],
                "warnings": [],
            }

        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            for value in nums
        ):
            return {
                "valid": False,
                "errors": ["Array must contain numeric values."],
                "warnings": [],
            }

        if any(nums[i] > nums[i + 1] for i in range(len(nums) - 1)):
            return {
                "valid": False,
                "errors": ["Binary Search requires a sorted array."],
                "warnings": [],
            }

        if not isinstance(steps, list) or not steps:
            return {
                "valid": False,
                "errors": ["Trace must contain at least one step."],
                "warnings": [],
            }

        previous_step = None
        found = False
        actual_found_index = None

        for step_number, step in enumerate(steps, start=1):

            if not isinstance(step, dict):
                errors.append(
                    f"Step {step_number}: Step must be a dictionary."
                )
                break

            required = ("left", "right", "mid")

            if any(key not in step for key in required):
                errors.append(
                    f"Step {step_number}: Missing required fields."
                )
                break

            left = step["left"]
            right = step["right"]
            mid = step["mid"]

            if any(
                not isinstance(value, int) or isinstance(value, bool)
                for value in (left, right, mid)
            ):
                errors.append(
                    f"Step {step_number}: Indices must be integers."
                )
                break

            if not (0 <= left <= right < len(nums)):
                errors.append(
                    f"Step {step_number}: Invalid search boundaries."
                )
                break

            expected_mid = left + (right - left) // 2

            if mid != expected_mid:
                errors.append(
                    f"Step {step_number}: Incorrect mid. "
                    f"Expected {expected_mid}, received {mid}."
                )
                break

            actual_value = nums[mid]

            if "value" in step and step["value"] != actual_value:
                errors.append(
                    f"Step {step_number}: Incorrect array value. "
                    f"Expected {actual_value}, "
                    f"received {step['value']}."
                )
                break

            if previous_step is not None:
                prev_left = previous_step["left"]
                prev_right = previous_step["right"]
                prev_mid = previous_step["mid"]
                prev_value = nums[prev_mid]

                if prev_value < target:
                    expected_bounds = (
                        prev_mid + 1,
                        prev_right,
                    )
                elif prev_value > target:
                    expected_bounds = (
                        prev_left,
                        prev_mid - 1,
                    )
                else:
                    errors.append(
                        f"Step {step_number}: Search continued "
                        "after target was found."
                    )
                    break

                actual_bounds = (left, right)

                if actual_bounds != expected_bounds:
                    errors.append(
                        f"Step {step_number}: Incorrect search "
                        f"boundaries. Expected {expected_bounds}, "
                        f"received {actual_bounds}."
                    )
                    break

            if actual_value == target:
                found = True
                actual_found_index = mid

                if step_number != len(steps):
                    errors.append(
                        "Trace contains steps after target was found."
                    )
                break

            previous_step = step

        if not errors and found:
            if reported_index is not None:
                if reported_index != actual_found_index:
                    errors.append(
                        f"Incorrect reported index. "
                        f"Expected {actual_found_index}, "
                        f"received {reported_index}."
                    )

        elif not errors and not found:
            if reported_index is not None:
                if (
                    not isinstance(reported_index, int)
                    or isinstance(reported_index, bool)
                    or not 0 <= reported_index < len(nums)
                    or nums[reported_index] != target
                ):
                    errors.append(
                        "Reported index does not contain the target."
                    )
                else:
                    warnings.append(
                        "Trace did not demonstrate finding the target."
                    )

        return {
            "valid": len(errors) == 0,
            "found": found,
            "actual_index": actual_found_index,
            "errors": errors,
            "warnings": warnings,
        }
