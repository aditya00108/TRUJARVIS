
"""
TRUJARVIS - Advanced LLM Engine

Handles local LLM communication, streaming,
generation parameters and conversation context.
"""

import ollama

from core.config import (
    OLLAMA_HOST,
    MODEL_NAME,
    TEMPERATURE,
    SYSTEM_PROMPT,
    MAX_HISTORY_MESSAGES,
)


class LLMEngine:

    def __init__(self):

        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

        self.model = MODEL_NAME

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

        try:

            self.client.list()

            return True, "Ollama connected successfully."

        except Exception as error:

            return False, str(error)

    # ------------------------------------------
    # AVAILABLE MODELS
    # ------------------------------------------

    def get_available_models(self):

        try:

            response = self.client.list()

            return [
                model.model
                for model in response.models
            ]

        except Exception as error:

            raise RuntimeError(
                f"Unable to retrieve models: {error}"
            ) from error

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
    # STREAMING RESPONSE GENERATION
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

        recent_messages = messages[-MAX_HISTORY_MESSAGES:]

        active_system_prompt = (
            system_prompt
            if system_prompt is not None
            else SYSTEM_PROMPT
        )

        formatted_messages = [
            {
                "role": "system",
                "content": active_system_prompt
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

            stream = self.client.chat(
                model=active_model,
                messages=formatted_messages,
                stream=True,
                options=options,
            )

            for chunk in stream:

                content = chunk.message.content

                if content:
                    yield content

        except Exception as error:

            raise RuntimeError(
                f"TRUJARVIS AI Engine Error: {error}"
            ) from error
