
# TRUJARVIS - System Architecture

## 1. Project Overview

TRUJARVIS (AI for Everything) is a modular AI assistant
built using Python, Streamlit, Ollama and SQLite.

The current implementation uses a locally hosted
Llama 3.2 model through Ollama.

## 2. Current Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| LLM Runtime | Ollama |
| AI Model | Llama 3.2 |
| Database | SQLite |
| Python Version | 3.12 |

## 3. Project Structure

```text
TRUJARVIS/
├── app.py
├── core/
│   ├── config.py
│   └── llm_engine.py
├── database/
│   └── db.py
├── tests/
├── modules/
├── assets/
├── requirements.txt
└── README.md
```

## 4. Core Components

### Frontend - app.py
Handles the Streamlit interface, chat interactions,
sidebar navigation and model settings.

### Configuration - core/config.py
Maintains centralized application configuration,
including model name, Ollama host, temperature,
conversation history limit and system prompt.

### AI Engine - core/llm_engine.py
Manages communication with Ollama and generates
streaming responses from the selected language model.

### Database - database/db.py
Handles SQLite-based conversation and message
persistence.

### Tests - tests/
Contains tests for database operations and AI engine
functionality.

## 5. Current AI Workflow

1. User enters a message through Streamlit.
2. Application retrieves conversation history.
3. User message is saved in SQLite.
4. LLM Engine prepares the model input.
5. Ollama processes the request using Llama 3.2.
6. Generated response is streamed to Streamlit.
7. Assistant response is saved in SQLite.

## 6. Future Architecture Plans

The following capabilities are planned, not yet
implemented:

- Cloud LLM provider integration
- Hybrid local and cloud inference
- Retrieval-Augmented Generation (RAG)
- PDF document understanding
- Long-term conversational memory
- Voice input and output
- Vision capabilities
- AI agent workflows

