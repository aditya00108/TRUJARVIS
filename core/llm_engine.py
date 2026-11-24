
"""
TRUJARVIS - Advanced LLM Engine

Connects ModelRouter with the Response Quality Layer.
Preserves the existing Streamlit generator interface.
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

    def __init__(self):

        # Initialize ModelRouter
        self.router = ModelRouter()

        # Register Ollama provider
        self.router.register_provider(
            name="ollama",
            provider=OllamaProvider(),
            make_default=True,
        )

        # Initialize Quality Controller
        self.quality_controller = QualityController()

        # Store the latest validation report
        self.last_quality_report = None

        self.model = MODEL_NAME

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
    # RESPONSE GENERATION + QUALITY VALIDATION
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

        # Limit conversation history
        recent_messages = messages[-MAX_HISTORY_MESSAGES:]

        # Prepare system prompt
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

        # Prepare generation options
        options = self.build_options(
            temperature=temperature,
            top_p=top_p,
            num_ctx=num_ctx,
            num_predict=num_predict,
            repeat_penalty=repeat_penalty,
        )

        active_model = model or self.model

        try:

            # Generate complete response through ModelRouter
            response_parts = self.router.generate_response(
                messages=formatted_messages,
                model=active_model,
                options=options,
                provider_name="ollama",
            )

            complete_response = "".join(response_parts)

            # Validate the generated response
            self.last_quality_report = (
                self.quality_controller.validate_response(
                    complete_response
                )
            )

            # Preserve generator compatibility with Streamlit
            if complete_response:
                yield complete_response

        except Exception as error:

            raise RuntimeError(
                f"TRUJARVIS AI Engine Error: {error}"
            ) from error
