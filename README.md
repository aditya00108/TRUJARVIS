# 🤖 TRUJARVIS | AI for Everything

**A Modular AI-Powered Personal Assistant built with Python, Streamlit, Ollama and SQLite.**

TRUJARVIS is an AI assistant designed to bring multiple AI capabilities together through a unified interface. The project currently uses a locally hosted Llama 3.2 model through Ollama, with a modular architecture designed to support future cloud AI integrations and intelligent automation.

---

## 🚀 Current Features

- **AI Chat Interface:** Interactive chatbot powered by Streamlit.
- **Local LLM Integration:** Runs Llama 3.2 through Ollama.
- **Streaming Responses:** Displays AI responses progressively.
- **Conversation Persistence:** Stores chat history using SQLite.
- **Chat Management:** Create, rename and delete conversations.
- **Advanced Model Settings:** Configure temperature, Top P, context window, response tokens and repeat penalty.
- **Modular Architecture:** Separates application, AI engine, configuration and database logic.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| Streamlit | Web application interface |
| Ollama | Local LLM runtime |
| Llama 3.2 | Language model |
| SQLite | Conversation storage |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
TRUJARVIS/
│
├── app.py
├── core/
│   ├── config.py
│   ├── llm_engine.py
│   └── __init__.py
│
├── database/
│   └── db.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT_LOG.md
│
├── modules/
├── assets/
├── tests/
│   ├── test_advanced_engine.py
│   ├── test_database.py
│   └── test_llm.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.12
- Git
- Ollama

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd TRUJARVIS
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

Download Ollama from:

https://ollama.com/

Pull the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Ensure the Ollama service is running.

### 5. Launch TRUJARVIS

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🧠 AI Configuration

The centralized configuration is maintained in:

`core/config.py`

Current default configuration:

| Parameter | Value |
|---|---|
| Model | llama3.2:latest |
| Temperature | 0.7 |
| Maximum History Messages | 20 |
| Ollama Host | localhost:11434 |

Additional generation parameters can be adjusted through the Advanced Model Settings panel.

## 🧪 Testing

Run the advanced engine test:

```bash
python -m tests.test_advanced_engine
```

Run the database test:

```bash
python -m tests.test_database
```

## 🗺️ Development Roadmap

The following capabilities are planned for future development:

- [ ] Hybrid local and cloud AI architecture
- [ ] Groq, Gemini and Cloudflare Workers AI integration
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] PDF document understanding
- [ ] Long-term conversational memory
- [ ] Voice input and output
- [ ] Vision capabilities
- [ ] AI agent workflows
- [ ] Multi-provider model management

## 💻 Development Philosophy

TRUJARVIS follows a modular development approach with an emphasis on:

- Open-source technologies and free resources wherever practical.
- Efficient use of local hardware.
- Cloud alternatives for computationally intensive workloads.
- Secure API key management.
- Maintainable and testable code.

## 📚 Documentation

- [System Architecture](docs/ARCHITECTURE.md)
- [Development Log](docs/DEVELOPMENT_LOG.md)

## 📌 Project Status

**Version:** 1.0.0

**Status:** Active Development

TRUJARVIS is an evolving project. Features listed under the roadmap are planned and should not be considered implemented until verified.

---

*TRUJARVIS | AI for Everything*