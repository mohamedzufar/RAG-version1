from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class DocumentStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"
    include_sources: bool = True

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]
    confidence: float
    latency_ms: float
    session_id: str
    cached: bool = False
    cost: float = 0.04

class DocumentUploadResponse(BaseModel):
    filename: str
    chunk_count: int
    status: DocumentStatus
    message: str

class MetricsResponse(BaseModel):
    total_queries: int
    avg_latency_ms: float
    p95_latency_ms: float
    cache_hit_rate: float
    avg_confidence: float
    total_cost: float