
"""
TRUJARVIS - Advanced LLM Engine

Handles model routing, response generation,
quality validation and automatic self-correction.
"""

from core.config import (
    MODEL_NAME,
    TEMPERATURE,
    SYSTEM_PROMPT,
    MAX_HISTORY_MESSAGES,
)

from core.model_router import ModelRouter
from core.quality.quality_controller import QualityController
from providers.ollama_provider import OllamaProvider


class LLMEngine:

    MAX_RETRIES = 2

    def __init__(self):

        # Initialize ModelRouter
        self.router = ModelRouter()

        self.router.register_provider(
            name="ollama",
            provider=OllamaProvider(),
            make_default=True,
        )

        # Initialize Quality Controller
        self.quality_controller = QualityController()

        self.model = MODEL_NAME

        # Quality reports
        self.last_quality_report = None
        self.attempt_reports = []

        # Default generation settings
        self.default_options = {
            "temperature": TEMPERATURE,
            "top_p": 0.9,
            "num_ctx": 2048,
            "num_predict": 512,
            "repeat_penalty": 1.1,
        }

    # ------------------------------------------
    # CONNECTION CHECK
    # ------------------------------------------

    def check_connection(self):
        return self.router.check_connection()

    # ------------------------------------------
    # AVAILABLE MODELS
    # ------------------------------------------

    def get_available_models(self):
        return self.router.list_models()

    # ------------------------------------------
    # GENERATION OPTIONS
    # ------------------------------------------

    def build_options(
        self,
        temperature=None,
        top_p=None,
        num_ctx=None,
        num_predict=None,
        repeat_penalty=None,
    ):

        options = self.default_options.copy()

        custom_options = {
            "temperature": temperature,
            "top_p": top_p,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "repeat_penalty": repeat_penalty,
        }

        for key, value in custom_options.items():
            if value is not None:
                options[key] = value

        return options

    # ------------------------------------------
    # INTERNAL RESPONSE GENERATION
    # ------------------------------------------

    def _generate_complete_response(
        self,
        messages,
        model,
        options,
    ):
        """Generate and collect a complete model response."""

        response_parts = self.router.generate_response(
            messages=messages,
            model=model,
            options=options,
            provider_name="ollama",
        )

        return "".join(response_parts)

    # ------------------------------------------
    # SELF-CORRECTION PROMPT
    # ------------------------------------------

    @staticmethod
    def _build_correction_prompt(response, report):

        error_details = "\n".join(
            f"- {error}" for error in report["errors"]
        )

        return f"""
Your previous response failed quality validation.

Validation errors:
{error_details}

Previous response:
{response}

Please correct the specific errors listed above.

Instructions:
1. Preserve the original user's requirements.
2. Correct the identified errors.
3. Return the complete corrected response.
4. Do not merely explain the errors.
5. Do not claim that the response is verified unless it is.
"""

    # ------------------------------------------
    # STREAMING RESPONSE + SELF-CORRECTION
    # ------------------------------------------

    def generate_response(
        self,
        messages,
        temperature=None,
        top_p=None,
        num_ctx=None,
        num_predict=None,
        repeat_penalty=None,
        system_prompt=None,
        model=None,
    ):

        if not messages:
            raise ValueError(
                "Conversation messages cannot be empty."
            )

        # Reset previous reports
        self.last_quality_report = None
        self.attempt_reports = []

        # Prepare conversation history
        recent_messages = messages[-MAX_HISTORY_MESSAGES:]

        active_system_prompt = (
            system_prompt
            if system_prompt is not None
            else SYSTEM_PROMPT
        )

        formatted_messages = [
            {
                "role": "system",
                "content": active_system_prompt,
            }
        ] + recent_messages

        options = self.build_options(
            temperature=temperature,
            top_p=top_p,
            num_ctx=num_ctx,
            num_predict=num_predict,
            repeat_penalty=repeat_penalty,
        )

        active_model = model or self.model

        try:

            # Initial generation + maximum two retries
            for attempt in range(self.MAX_RETRIES + 1):

                complete_response = (
                    self._generate_complete_response(
                        messages=formatted_messages,
                        model=active_model,
                        options=options,
                    )
                )

                # Validate response
                report = self.quality_controller.validate_response(
                    complete_response
                )

                report["attempt"] = attempt + 1
                self.attempt_reports.append(report)

                self.last_quality_report = report

                # Return when validation succeeds
                if report["valid"]:
                    yield complete_response
                    return

                # Stop if retry limit reached
                if attempt == self.MAX_RETRIES:
                    break

                # Build correction request
                correction_prompt = (
                    self._build_correction_prompt(
                        complete_response,
                        report,
                    )
                )

                # Add previous response and correction instruction
                formatted_messages = (
                    formatted_messages
                    + [
                        {
                            "role": "assistant",
                            "content": complete_response,
                        },
                        {
                            "role": "user",
                            "content": correction_prompt,
                        },
                    ]
                )

            # Return final response even if validation failed.
            # The quality report clearly records its status.
            if self.attempt_reports:
                final_response = complete_response
                yield final_response

        except Exception as error:

            raise RuntimeError(
                f"TRUJARVIS AI Engine Error: {error}"
            ) from error
