import os
from dotenv import load_dotenv  # ✅ Add this
from pydantic_settings import BaseSettings
from typing import Optional

# ✅ Load .env file
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "RAG Production"
    APP_VERSION: str = "1.0.0"
    
    LLM_MODEL: str = "gemma3:1b"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    CHUNK_SIZE: int = 200
    CHUNK_OVERLAP: int = 50
    
    RETRIEVAL_K: int = 5
    RERANK_TOP_K: int = 2
    SIMILARITY_THRESHOLD: float = 0.75
    
    # ✅ Read from environment
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "rag-assistant")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east1-gcp")
    
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_TTL: int = 3600
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()