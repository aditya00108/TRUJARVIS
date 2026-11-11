
"""
TRUJARVIS - Application Configuration
Centralized settings for the application.
"""

APP_NAME = "TRUJARVIS"
APP_VERSION = "1.0.0"

# Ollama configuration
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "llama3.2:latest"

# Generation settings
TEMPERATURE = 0.7
MAX_HISTORY_MESSAGES = 20

# Assistant personality
SYSTEM_PROMPT = """
You are TRUJARVIS, an intelligent personal AI assistant.

Your responsibilities:
1. Answer questions clearly and accurately.
2. Explain complex concepts in simple language.
3. Help with programming and technical tasks.
4. Maintain conversational context.
5. Be professional, helpful and friendly.

Always prioritize accuracy. If you do not know something,
say so instead of inventing information.
"""
