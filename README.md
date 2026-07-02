# 🎙️ SmartMinutes

AI-powered meeting intelligence platform that transforms conversations into searchable knowledge through transcription, summarization, action extraction, and Retrieval-Augmented Generation (RAG).

🔗 **Live Demo:** :contentReference[oaicite:0]{index=0}

---

## ✨ Features

- Multi-agent AI workflow orchestration
- Audio and video meeting uploads
- Speaker diarization and timestamped transcripts
- Executive and topic-wise summaries
- Automatic action item extraction
- RAG-powered semantic search with citations
- Interactive agent execution dashboard
- Speaker analytics and meeting insights
- JWT authentication and secure APIs
- Dockerized deployment setup

---

## 🏗️ Architecture

```text
Upload
   │
   ▼
Coordinator Agent
   │
   ├── Transcription Agent
   ├── Summarization Agent
   ├── Action Extraction Agent
   └── Retrieval Agent
            │
            ▼
PostgreSQL + ChromaDB
            │
            ▼
     RAG Search Interface
```

---

## 🛠️ Tech Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- Lucide React

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication

### AI & ML
- OpenAI
- Whisper / WhisperX
- LangChain
- Sentence Transformers
- ChromaDB

### Infrastructure
- PostgreSQL
- Docker
- Celery
- Redis

---

## 📂 Project Structure

```text
smartminutes/
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── app/
│       ├── components/
│       ├── data/
│       └── utils/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── models/
│       ├── schemas/
│       └── main.py
│
├── ai_services/
│   ├── coordinator.py
│   ├── transcription.py
│   ├── summarization.py
│   ├── action_items.py
│   └── retrieval.py
│
├── database/
│   └── schema.sql
│
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── docker-compose.yml
│
└── README.md
```

---

## 🚀 Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker

```bash
docker-compose up --build
```

---

## 🤖 Multi-Agent Workflow

| Agent | Responsibility |
|--------|----------------|
| Coordinator | Orchestrates the complete pipeline |
| Transcription | Speech-to-text and diarization |
| Summarization | Executive summaries and insights |
| Action Extraction | Tasks, owners, and deadlines |
| Retrieval | Embeddings and semantic search |

---

## 🔍 Example Query

```text
User:
What decisions were made about the mobile application redesign?

Response:
The team agreed to migrate to React Native,
prioritize accessibility improvements,
and schedule a beta release for Q4.

Sources:
Meeting_12_Aug_2025 [12:45]
Meeting_18_Aug_2025 [27:10]
```

---

## 📌 Engineering Highlights

- Multi-agent AI architecture
- Retrieval-Augmented Generation (RAG)
- FastAPI + PostgreSQL backend design
- JWT-based authentication
- Background processing with Celery
- Interactive Next.js dashboard
- Dockerized deployment pipeline

---

## 👩‍💻 Author

**Tisha Mahato**

Full-Stack Developer • AI Engineer • Technical Writer


---

⭐ If you found this project interesting, consider giving it a star.
