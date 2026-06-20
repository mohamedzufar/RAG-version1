from typing import List, Dict
from sentence_transformers import CrossEncoder
from app.config import settings
import time

class RetrievalPipeline:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.reranker = CrossEncoder("BAAI/bge-reranker-base")
        self.latency_history = []
    
    def hybrid_search(self, query: str) -> Dict:
        start = time.time()
        
        # Vector search
        results = self.vector_store.similarity_search_with_score(
            query, k=settings.RETRIEVAL_K * 2
        )
        
        # Re-rank
        if results:
            pairs = [(query, doc.page_content) for doc, _ in results]
            scores = self.reranker.predict(pairs)
            
            ranked = []
            for i, (doc, _) in enumerate(results):
                ranked.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(scores[i])
                })
            
            ranked.sort(key=lambda x: x["score"], reverse=True)
            top_results = ranked[:settings.RERANK_TOP_K]
            confidence = top_results[0]["score"] if top_results else 0.0
        else:
            top_results = []
            confidence = 0.0
        
        latency = (time.time() - start) * 1000
        self.latency_history.append(latency)
        
        return {
            "results": top_results,
            "confidence": min(max(confidence, 0.0), 1.0),
            "latency_ms": latency
        }