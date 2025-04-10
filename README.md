# 🧠 Intelligent Document Upload and Q&A System

## 📚 Overview

This is a full-stack application that allows users to upload documents (PDF, CSV, PPT, etc.), parse and store them, and ask natural language questions based on the contents using a Retrieval-Augmented Generation (RAG) pipeline with Google's Gemini model.

## ⚙️ Technologies Used

### 🖥️ Frontend

- React.js (with Bootstrap 5 for UI)
- AuthContext for session management
- Two entry points: Login & Signup (authentication)

### 🚀 Backend

- FastAPI (REST API framework)
- LangChain + LlamaIndex (RAG pipeline)
- Google Gemini via `langchain-google-genai`
- FAISS (vector store for embedding search)
- Elasticsearch (semantic document retrieval)
- MinIO (S3-compatible file storage)
- Redis (JWT/session storage)
- unstructured.io (document parsing)

### 🐳 DevOps & Deployment

- Docker (for containerized deployment)
- Docker Compose (multi-service orchestration)
- JWT Authentication (access token issued via Redis)

## ✅ Features

- User Signup/Login with JWT auth
- Upload and parse documents (PDF, CSV, etc.)
- Store files securely on MinIO
- Index parsed text with Gemini embeddings (Google Generative AI)
- Semantic query answering with LangChain's RetrievalQA
- Real-time vector-based search using Elasticsearch
- Responsive frontend with Bootstrap 5

## 🧠 NLP Pipeline

1. User uploads documents from frontend
2. FastAPI backend stores file in MinIO and parses using unstructured.io
3. Text is chunked and embedded using GoogleGenerativeAIEmbeddings
4. Chunks stored in FAISS vector database
5. Query sent from frontend to backend
6. Backend performs semantic search with Elasticsearch
7. Top relevant docs passed to Gemini via LangChain RetrievalQA
8. Gemini generates and returns final answer

## 🧱 High-Level Architecture Diagram

```
                        ┌─────────────────────────────┐
                        │         React Frontend      │
                        │  - Login & Signup           │
                        │  - Upload Page              │
                        │  - Ask Question Interface   │
                        └────────────┬────────────────┘
                                     │ REST (JWT Auth)
                                     ▼
                        ┌─────────────────────────────┐
                        │         FastAPI Backend      │
                        │  - Auth (/signup, /login)    │
                        │  - /upload, /ask endpoints   │
                        └───────┬────────────┬────────┘
                                │            │
               ┌────────────────┘            └────────────────┐
               ▼                                             ▼
       ┌─────────────┐                               ┌────────────────┐
       │ MinIO (S3)  │                               │ Redis (JWT)    │
       └─────────────┘                               └────────────────┘
               │
               ▼
      ┌──────────────────┐
      │ unstructured.io  │ (parsing)
      └──────────────────┘
               │
               ▼
    ┌────────────────────────────┐
    │  Google Embeddings (Gemini)│
    └────────────────────────────┘
               │
               ▼
         ┌────────────┐
         │   FAISS    │ (Vector DB)
         └────┬───────┘
              │
              ▼
       ┌───────────────┐
       │ Elasticsearch │ (RAG Search)
       └───────────────┘
```

## 🔧 Low-Level Design (LLD)

- **Frontend (React.js)**

  - `AuthContext.js`: manages login state and token storage
  - `Login.js`, `Signup.js`: handle auth via API calls to backend
  - `Upload.js`: allows users to upload documents (calls `/upload` endpoint)
  - `Ask.js`: takes user query and calls `/ask` endpoint to retrieve answer

- **Backend (FastAPI)**

  - `main.py`: entry point for FastAPI app, includes CORS and routing setup
  - `auth.py`: handles user registration, login, and token issuance via Redis
  - `upload.py`: parses uploaded files using unstructured.io and stores them in MinIO
  - `ask.py`: processes user query through RAG pipeline
  - `utils/jwt.py`: token creation and validation logic
  - `utils/elasticsearch.py`: interfaces with Elasticsearch

- **NLP (LangChain + Gemini)**

  - `GoogleGenerativeAIEmbeddings`: used to embed document chunks
  - `RetrievalQA`: chain used for querying Gemini with top docs
  - `FAISS`: stores and retrieves vectorized document chunks

## 🐳 Docker Deployment

### 📁 Project Structure

```
project-root/
├── backend/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
├── doc-rag-ui/ (React frontend with auth)
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
├── docker-compose.yml
```

### 🐳 Dockerfile (Backend - FastAPI)

```Dockerfile
FROM python:3.11

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libpoppler-cpp-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pip & tooling
RUN pip install --upgrade pip wheel setuptools

COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY .env .env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```

### 🐳 Dockerfile (Frontend - React)

```Dockerfile

FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "3000"]

```

### 🧩 docker-compose.yml

```yaml


services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=Your_api_key_here
    depends_on:
      - redis
      - elasticsearch
      - minio

  frontend-auth:
    build: ./doc-rag-ui
    ports:
    - "3000:3000"
    depends_on:
      - backend

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - xpack.security.http.ssl.enabled=false
    ports:
      - "9200:9200"

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio-data:/data
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server --console-address ":9001" /data

volumes:
  minio-data:

```

## 🔒 Authentication

- User starts at Login or Signup page in frontend
- FastAPI `/signup` saves user info in Redis (hashed with bcrypt)
- `/login` validates and returns JWT token
- Token stored in browser `localStorage`
- Token used in Authorization headers for secure endpoints

## 📄 API Documentation

FastAPI automatically generates interactive API docs:

- 📘 **Swagger UI**:\
  Access it at [http://localhost:8000/docs](http://localhost:8000/docs)\
  Provides a user-friendly interface to test all backend routes like `/signup`, `/login`, `/upload`, `/ask`.

- 📗 **ReDoc**:\
  Available at [http://localhost:8000/redoc](http://localhost:8000/redoc)\
  Offers an alternate, neatly organized API reference view.

These tools allow you to:

- View request and response formats
- Try endpoints directly in the browser
- See error codes and auth requirements

## 👏 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [Google Generative AI](https://ai.google.dev/)
- [unstructured.io](https://github.com/Unstructured-IO/unstructured)
- [FAISS](https://github.com/facebookresearch/faiss)
- [ElasticSearch](https://www.elastic.co/)

---


