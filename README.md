# Multi-Agent PoC

A proof-of-concept implementation of a **LangGraph-based multi-agent system** powered by FastAPI. This project demonstrates collaborative workflows between agents (e.g., Supervisor and Research Team) to complete complex tasks using LLMs, tools, and graph-based orchestration.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/sumitcoder01/multi-agent-poc.git
cd multi-agent-poc
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

* Local API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 5. Deactivate the Virtual Environment

```bash
deactivate
```

---

## ⚙️ Project Structure

```
multi-agent-poc/
│
├── app/
│   ├── agents/            # LangGraph-based agent definitions
│   ├── api/               # FastAPI endpoints
│   ├── llm/               # LLM client initialization
│   ├── tools/             # Custom tool functions
│   └── main.py            # FastAPI app entrypoint
│
├── venv/                  # Python virtual environment (excluded in .gitignore)
├── requirements.txt       # Python dependencies
└── README.md              # You're reading it!
```

---

## Built With

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [LangChain](https://github.com/langchain-ai/langchain)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* LLMs (via OpenAI, Groq, etc.)

---

## 📌 TODO

* [ ] Add memory to agents
* [ ] Integrate file upload & RAG capabilities
* [ ] Deploy to Render or Hugging Face Spaces
