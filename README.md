# 📚 RAG Knowledge Assistant

> A production-oriented Retrieval-Augmented Generation (RAG) system for intelligent document question answering using hybrid retrieval, reranking, local LLM inference, and a FastAPI backend.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=flat-square)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20Database-000000?style=flat-square)
![Redis](https://img.shields.io/badge/Redis-Caching-DC382D?style=flat-square&logo=redis&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 Overview

The **RAG Knowledge Assistant** is an API-first document question-answering system designed to retrieve relevant information from uploaded PDF documents and generate grounded answers using a local Large Language Model.

Instead of sending an entire document to an LLM, the system follows a multi-stage retrieval pipeline:

```text
PDF Document
     │
     ▼
Text Extraction
     │
     ▼
Document Chunking
     │
     ▼
Embedding Generation
     │
     ▼
Pinecone Vector Database
     │
     │
     └──────────────────────────────┐
                                    │
User Query                         │
     │                              │
     ▼                              │
Query Embedding                     │
     │                              │
     ├────────► Semantic Search ────┤
     │                              │
     └────────► BM25 Search ────────┤
                                    ▼
                            Hybrid Retrieval
                                    │
                                    ▼
                           Cross-Encoder Reranking
                                    │
                                    ▼
                              Top-K Context
                                    │
                                    ▼
                              Local LLM
                              (Ollama)
                                    │
                                    ▼
                           Answer + Sources
```

The project focuses on practical RAG engineering rather than a simple "LLM + prompt" implementation.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📄 PDF Ingestion | Extract text from uploaded PDF documents |
| ✂️ Chunking | Recursive text splitting with configurable overlap |
| 🧠 Embeddings | SentenceTransformer embeddings |
| 🔎 Semantic Search | Vector similarity retrieval using Pinecone |
| 🔤 BM25 Search | Keyword-based retrieval for exact terminology |
| 🔀 Hybrid Retrieval | Combines semantic and lexical retrieval |
| 🎯 Reranking | Cross-encoder based relevance reranking |
| 🤖 Local LLM | Ollama-based local inference |
| ⚡ Redis Cache | Caches repeated query responses |
| 🛡️ Circuit Breaker | Handles downstream service failures |
| 📊 Metrics | Tracks latency, confidence, and cache performance |
| 🔗 Source Citations | Returns retrieved document sources |
| 🚀 FastAPI | High-performance REST API |
| 🧪 Testing | Automated tests for core components |
| 🔐 Configurable | Environment-based configuration |

---

# 🧠 Why RAG?

A standalone LLM may not have access to private or domain-specific documents.

RAG solves this by retrieving relevant information from an external knowledge source and providing that information as context to the LLM.

```text
Traditional LLM

Question
   │
   ▼
LLM
   │
   ▼
Answer
```

```text
RAG

Question
   │
   ▼
Retriever
   │
   ▼
Relevant Documents
   │
   ▼
Context
   │
   ▼
LLM
   │
   ▼
Grounded Answer
```

This architecture helps reduce the need to place entire documents into the model context and provides a mechanism for source-aware answers.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      Client         │
                         │  REST API / HTTP    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │     Application     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
             ┌──────────────┐                ┌──────────────┐
             │ PDF Ingestion│                │ Chat / Query │
             └──────┬───────┘                └──────┬───────┘
                    │                               │
                    ▼                               ▼
             ┌──────────────┐                ┌──────────────┐
             │ Text Chunking│                │ Redis Cache  │
             └──────┬───────┘                └──────┬───────┘
                    │                               │
                    ▼                               ▼
             ┌──────────────┐                ┌──────────────┐
             │  Embeddings  │                │Hybrid Search │
             └──────┬───────┘                └──────┬───────┘
                    │                               │
                    ▼                        ┌──────┴──────┐
             ┌──────────────┐                │             │
             │   Pinecone   │◄───────────────┤             │
             │ Vector Store │                ▼             ▼
             └──────────────┘          Semantic Search  BM25
                                             │             │
                                             └──────┬──────┘
                                                    ▼
                                            ┌──────────────┐
                                            │  Reranker    │
                                            └──────┬───────┘
                                                   │
                                                   ▼
                                            ┌──────────────┐
                                            │    Ollama    │
                                            │   Local LLM  │
                                            └──────┬───────┘
                                                   │
                                                   ▼
                                            Answer + Sources
```

---

# 🔄 End-to-End Data Flow

## 1. Document Ingestion

A PDF is uploaded through the FastAPI endpoint.

```text
PDF
 ↓
Text Extraction
 ↓
Text Cleaning
 ↓
Recursive Chunking
 ↓
Embedding Generation
 ↓
Vector Storage
```

The default configuration uses:

- Chunk size: `200`
- Chunk overlap: `50`
- Embedding model: `all-MiniLM-L6-v2`
- Embedding dimension: `384`

---

## 2. Query Processing

When a user submits a question:

```text
User Query
    │
    ▼
Query Embedding
    │
    ├──────────────► Pinecone Semantic Search
    │
    └──────────────► BM25 Keyword Search
                            │
                            ▼
                     Candidate Documents
                            │
                            ▼
                    Hybrid Retrieval
                            │
                            ▼
                   Cross-Encoder Reranker
                            │
                            ▼
                       Top Results
                            │
                            ▼
                     Context Builder
                            │
                            ▼
                       Local LLM
                            │
                            ▼
                  Answer + Source Metadata
```

---

# 🔎 Retrieval Strategy

The project uses multiple retrieval stages rather than relying on a single similarity search.

### Semantic Retrieval

SentenceTransformer embeddings convert documents and queries into vector representations.

```text
Document
   ↓
Embedding
   ↓
384-dimensional Vector
   ↓
Pinecone
```

The query is embedded using the same embedding model and compared against indexed document vectors.

---

### BM25 Retrieval

BM25 provides lexical retrieval based on the actual terms present in the document.

This is useful for:

- Names
- Technical terms
- Product names
- IDs
- Exact phrases
- Domain-specific terminology

---

### Hybrid Retrieval

The system combines semantic and lexical retrieval:

```text
                User Query
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   Semantic Search         BM25 Search
          │                   │
          └─────────┬─────────┘
                    ▼
             Candidate Set
```

This provides two complementary retrieval signals.

---

### Cross-Encoder Reranking

Retrieved candidates are reranked using:

```text
BAAI/bge-reranker-base
```

The reranker evaluates the relationship between the query and retrieved text and produces a more focused ranking before context is sent to the LLM.

```text
Top Retrieval Candidates
          │
          ▼
    Cross Encoder
          │
          ▼
     Relevance Scores
          │
          ▼
      Top-K Context
```

---

# 🤖 Local LLM

The generation layer uses **Ollama** for local LLM inference.

Configured model:

```text
phi
```

The primary advantage is that the application does not require a paid external LLM API for answer generation.

The current architecture still uses **Pinecone as an external vector database**, so the system should not be described as completely offline or 100% local.

---

# 🧰 Technology Stack

## Backend

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic

## AI / ML

- Ollama
- Local `phi` model
- SentenceTransformers
- `all-MiniLM-L6-v2`
- `BAAI/bge-reranker-base`
- LangChain

## Retrieval

- Pinecone
- BM25
- Hybrid Retrieval
- Cross-Encoder Reranking

## Data Processing

- PyPDF / PyPDFLoader
- Recursive Character Text Splitter

## Caching

- Redis

## Testing

- Pytest
- HTTPX
- Pytest-Cov

---

# 📊 Evaluation & Performance

The current project benchmark reported the following values:

| Metric | Reported Value |
|---|---:|
| Answer Accuracy | ~84% |
| P95 Latency | ~320 ms |
| Cache Hit Rate | ~65% |
| Indexed Chunks | ~727 |
| Embedding Dimension | 384 |

> **Benchmark note:** These measurements are project-specific and depend on the dataset, hardware, model configuration, retrieval parameters, and evaluation methodology. They should not be interpreted as universal system performance.

---

# ⚡ Performance Optimization

The system exposes configurable retrieval parameters.

### Lower Latency Experiment

```env
CHUNK_SIZE=150
CHUNK_OVERLAP=30
RETRIEVAL_K=5
RERANK_TOP_K=3
```

### Higher Retrieval Coverage Experiment

```env
CHUNK_SIZE=500
CHUNK_OVERLAP=75
RETRIEVAL_K=20
RERANK_TOP_K=5
```

The optimal configuration depends on document structure and evaluation results.

---

# 🔌 API

The project exposes a REST API through FastAPI.

## Upload Document

```http
POST /upload
```

Uploads and indexes a PDF document.

Example:

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

Example response:

```json
{
  "filename": "document.pdf",
  "chunk_count": 120,
  "status": "success"
}
```

---

## Ask a Question

```http
POST /chat
```

Example:

```bash
curl -X POST \
  "http://localhost:8000/chat?query=What%20is%20the%20main%20topic%20of%20the%20document?"
```

Example response:

```json
{
  "answer": "The document discusses...",
  "confidence": 0.87,
  "latency_ms": 312,
  "sources": [
    {
      "source": "document.pdf",
      "page": 4
    }
  ]
}
```

---

## Health Check

```http
GET /health
```

Example:

```bash
curl http://localhost:8000/health
```

---

## Metrics

```http
GET /metrics
```

Example:

```bash
curl http://localhost:8000/metrics
```

Typical metrics include:

- Total queries
- Average latency
- P95 latency
- Cache hit rate
- Average confidence

---

# 📁 Project Structure

```text
RAG-version1/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── retrieval.py
│   │   └── generation.py
│   │
│   ├── cache/
│   │   └── redis_client.py
│   │
│   └── utils/
│       ├── fallback.py
│       └── metrics.py
│
├── data/
│   └── documents/
│
├── scripts/
│   ├── populate_db.py
│   └── evaluate.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   └── test_accuracy.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

---

# ⚙️ Prerequisites

Install the following before running the project:

- Python 3.11+
- Git
- Ollama
- Pinecone account
- Redis

Redis is used for caching and can be disabled or made optional depending on the application configuration.

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/mohamedzufar/RAG-version1.git
cd RAG-version1
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Configure Ollama

Install Ollama and start the local server:

```bash
ollama serve
```

Pull the configured LLM:

```bash
ollama pull phi
```

The embedding model is loaded through SentenceTransformers and does not need to be pulled through Ollama.

---

# 🔐 Environment Configuration

Create a `.env` file:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=rag-assistant

REDIS_URL=redis://localhost:6379
REDIS_TTL=3600

OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=phi

EMBEDDING_MODEL=all-MiniLM-L6-v2

CHUNK_SIZE=200
CHUNK_OVERLAP=50

RETRIEVAL_K=10
RERANK_TOP_K=3

SIMILARITY_THRESHOLD=0.75
```

### Pinecone Index

The configured Pinecone index should use:

```text
Dimension: 384
```

because `all-MiniLM-L6-v2` produces 384-dimensional embeddings.

---

# ▶️ Run the Application

Start Ollama:

```bash
ollama serve
```

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

---

# 🐍 Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Upload document
with open("document.pdf", "rb") as file:
    response = requests.post(
        f"{BASE_URL}/upload",
        files={"file": file}
    )

print(response.json())

# Ask question
response = requests.post(
    f"{BASE_URL}/chat",
    params={
        "query": "What is this document about?"
    }
)

print(response.json())
```

---

# 🛡️ Reliability Engineering

The application includes several mechanisms intended to improve operational reliability.

### Redis Caching

Repeated queries can be served from Redis instead of executing the complete retrieval and generation pipeline.

```text
Query
  │
  ▼
Redis Cache?
  │
  ├── HIT ──────► Cached Response
  │
  └── MISS
       │
       ▼
  Retrieval
       │
       ▼
  Reranking
       │
       ▼
  LLM Generation
       │
       ▼
  Store in Redis
       │
       ▼
  Response
```

---

### Circuit Breaker

The system can prevent repeated calls to an unavailable downstream service.

This is useful when dealing with:

- Ollama failures
- Vector database connectivity issues
- Temporary service interruptions

---

### Health Checks

The `/health` endpoint provides application-level health information and can be used by deployment infrastructure.

---

# 📊 Observability

The application tracks operational metrics such as:

```text
Total Queries
Average Latency
P95 Latency
Cache Hit Rate
Average Confidence
```

These metrics help evaluate retrieval and generation performance during development and testing.

---

# 🔐 Privacy & Security

The application is designed around local LLM inference.

### Local

- LLM inference through Ollama
- Embedding generation through SentenceTransformers
- Application processing through the local FastAPI service

### External

- Pinecone is currently used as the vector database.
- Therefore, indexed document representations are stored in the configured Pinecone environment.

For sensitive production deployments, infrastructure, data-retention, access-control, encryption, and vendor policies should be reviewed according to the deployment requirements.

Never commit secrets to Git:

```text
.env
API keys
credentials
tokens
private certificates
```

---

# ⚠️ Current Limitations

The current implementation has several limitations:

- Pinecone requires external connectivity.
- No web-based UI is currently included.
- Authentication and authorization are not fully implemented.
- Multi-user isolation is not currently implemented.
- Conversation memory is not currently implemented.
- Production deployment configuration is still evolving.
- Benchmark results are dataset and hardware dependent.
- RAG quality depends heavily on document parsing, chunking, retrieval, reranking, and evaluation methodology.

---

# 🗺️ Roadmap

## Completed

- [x] PDF ingestion
- [x] Recursive chunking
- [x] SentenceTransformer embeddings
- [x] Pinecone vector storage
- [x] Semantic retrieval
- [x] BM25 retrieval
- [x] Hybrid retrieval
- [x] Cross-encoder reranking
- [x] Local LLM inference
- [x] FastAPI backend
- [x] Redis caching
- [x] Circuit breaker
- [x] Metrics
- [x] Health checks
- [x] Source metadata

## In Progress

- [ ] Docker containerization
- [ ] Improved test coverage
- [ ] Authentication
- [ ] Multi-user support
- [ ] Conversation memory

## Planned

- [ ] Cloud deployment
- [ ] Document management API
- [ ] Advanced evaluation pipeline
- [ ] Improved reranking
- [ ] Graph RAG
- [ ] Agentic RAG
- [ ] Document explorer
- [ ] Export and sharing
- [ ] Production observability
- [ ] CI/CD pipeline

---

# 🧪 RAG Evaluation

A RAG system should be evaluated at multiple stages rather than using only final-answer accuracy.

Recommended evaluation dimensions:

```text
Document Retrieval
      │
      ├── Recall@K
      ├── Precision@K
      └── MRR

Reranking
      │
      ├── Relevance
      └── Ranking Quality

Generation
      │
      ├── Faithfulness
      ├── Answer Relevance
      └── Context Relevance

System
      │
      ├── Latency
      ├── Throughput
      ├── Cache Hit Rate
      └── Resource Usage
```

---

# 💡 Engineering Principles

This project follows several practical AI engineering principles:

### Retrieval Before Generation

The LLM should receive relevant context rather than the entire document whenever possible.

### Multiple Retrieval Signals

Semantic retrieval and lexical retrieval provide complementary search behavior.

### Reranking

Initial retrieval can produce noisy candidates. A reranker provides an additional relevance-filtering stage.

### Caching

Repeated queries should avoid unnecessary computation where possible.

### Observability

RAG systems should measure retrieval and generation behavior rather than treating the LLM as a black box.

### Configuration

Retrieval and generation parameters should be configurable rather than hard-coded.

---

# 📌 Example Use Cases

The architecture can be adapted for:

- 📚 Research paper assistants
- 🏢 Enterprise knowledge assistants
- 📄 Document Q&A
- 📑 Policy and compliance document search
- 🧾 Invoice and financial document analysis
- 🎓 Educational document assistants
- 💼 Internal company knowledge bases
- 🔧 Technical documentation assistants

---

# 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/your-feature
```

Make your changes, add tests where appropriate, and create a pull request.

Recommended commit style:

```text
feat: add hybrid retrieval
fix: improve document ingestion
refactor: simplify retrieval pipeline
test: add reranking tests
docs: update installation guide
```

---

# 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# 👨‍💻 Author

**Mohamed Zufar**

GitHub:

https://github.com/mohamedzufar

Repository:

https://github.com/mohamedzufar/RAG-version1.git

---

# ⭐ Project Summary

**RAG Knowledge Assistant** demonstrates an end-to-end RAG architecture combining:

```text
FastAPI
   +
PDF Processing
   +
SentenceTransformers
   +
Pinecone
   +
BM25
   +
Hybrid Retrieval
   +
Cross-Encoder Reranking
   +
Ollama
   +
Redis
   +
Evaluation
   +
Observability
```

The project is designed as an **API-first AI engineering system**, with emphasis on retrieval quality, modular architecture, local LLM inference, reliability, caching, and measurable performance.