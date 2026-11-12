
"""
TRUJARVIS - Code Validator

Extracts code blocks and validates
Python and C++ syntax.
"""

import ast
import re
import subprocess
import tempfile
from pathlib import Path


class CodeValidator:
    """Validates Python and C++ code syntax."""

    @staticmethod
    def extract_code_blocks(response: str) -> list:
        """Extract fenced code blocks from an AI response."""

        if not isinstance(response, str):
            return []

        pattern = r"```(\w+)?\s*\n(.*?)```"

        matches = re.findall(
            pattern,
            response,
            flags=re.DOTALL
        )

        return [
            {
                "language": (language or "").lower(),
                "code": code.strip()
            }
            for language, code in matches
        ]

    @staticmethod
    def validate_python(code: str) -> dict:
        """Validate Python syntax using AST."""

        try:
            ast.parse(code)

            return {
                "valid": True,
                "language": "python",
                "error": None,
            }

        except SyntaxError as error:

            return {
                "valid": False,
                "language": "python",
                "error": (
                    f"Line {error.lineno}: {error.msg}"
                ),
            }

    @staticmethod
    def validate_cpp(code: str) -> dict:
        """Validate C++ syntax using the installed g++ compiler."""

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".cpp",
                encoding="utf-8",
                delete=False,
            ) as temp_file:

                temp_file.write(code)
                temp_path = Path(temp_file.name)

            result = subprocess.run(
                [
                    "g++",
                    "-std=c++11",
                    "-fsyntax-only",
                    str(temp_path),
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:

                return {
                    "valid": True,
                    "language": "cpp",
                    "error": None,
                }

            return {
                "valid": False,
                "language": "cpp",
                "error": result.stderr.strip(),
            }

        except FileNotFoundError:

            return {
                "valid": False,
                "language": "cpp",
                "error": "g++ compiler not found.",
            }

        except subprocess.TimeoutExpired:

            return {
                "valid": False,
                "language": "cpp",
                "error": "Compilation check timed out.",
            }

        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink()

    @classmethod
    def validate_code(cls, code: str, language: str) -> dict:
        """Validate code according to its language."""

        language = language.lower().strip()

        if language in ("python", "py"):
            return cls.validate_python(code)

        if language in ("cpp", "c++", "cc", "cxx"):
            return cls.validate_cpp(code)

        return {
            "valid": False,
            "language": language,
            "error": "Unsupported programming language.",
        }

    @classmethod
    def validate_response(cls, response: str) -> list:
        """Extract and validate supported code blocks."""

        results = []

        for block in cls.extract_code_blocks(response):

            language = block["language"]

            if language in (
                "python", "py",
                "cpp", "c++", "cc", "cxx"
            ):

                result = cls.validate_code(
                    block["code"],
                    language
                )

                results.append(result)

        return results

