import os
import shutil
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.rag.ingestion import IngestionPipeline
from app.rag.retrieval import RetrievalPipeline
from app.rag.generation import GenerationPipeline

# Initialize
ingestion = IngestionPipeline()
retrieval = RetrievalPipeline(ingestion.vector_store)
generation = GenerationPipeline()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("data", exist_ok=True)

@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "status": "running"
    }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files")
    
    file_path = os.path.join("data", file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    chunk_count = ingestion.process_pdf(file_path)
    return {
        "filename": file.filename,
        "chunk_count": chunk_count,
        "status": "completed"
    }

@app.post("/chat")
async def chat(query: str, session_id: str = "default"):
    start = time.time()
    
    result = retrieval.hybrid_search(query)
    results = result["results"]
    confidence = result["confidence"]
    
    if not results or confidence < 0.75:
        return {
            "answer": "I don't have enough information.",
            "confidence": confidence,
            "latency_ms": (time.time() - start) * 1000
        }
    
    context = "\n\n".join([r["content"] for r in results])
    answer = generation.generate(context, query)
    
    return {
        "answer": answer,
        "confidence": confidence,
        "latency_ms": (time.time() - start) * 1000,
        "sources": results
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "chunks": ingestion.get_total_chunks()
    }