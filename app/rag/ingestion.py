import os
import time
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from app.config import settings
import logging
import numpy as np

logger = logging.getLogger(__name__)

# Custom embedding class for SentenceTransformer
class SentenceTransformerEmbeddings:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        return self.model.encode(texts, convert_to_numpy=True).tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        return self.model.encode(text, convert_to_numpy=True).tolist()

class IngestionPipeline:
    def __init__(self):
        # ✅ Use custom embedding class
        self.embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.vector_store = None
        self.total_chunks = 0
        self._init_pinecone()
    
    def _init_pinecone(self):
        try:
            # ✅ REPLACE with your actual API key
            PINECONE_API_KEY = "pcsk_2fVgG2_R1HLMMMZxXak8X85gDujBxFwxKcwSnJGFbuiPagvGTT38gWTVhacJ4HTUguA7Yi"
            
            print("🔑 Connecting to Pinecone...")
            
            pc = Pinecone(api_key=PINECONE_API_KEY)
            
            indexes = pc.list_indexes()
            index_names = [idx.name for idx in indexes]
            print(f"📋 Existing indexes: {index_names}")
            
            if settings.PINECONE_INDEX_NAME not in index_names:
                print(f"📌 Creating index: {settings.PINECONE_INDEX_NAME}")
                pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=384,  # all-MiniLM-L6-v2 uses 384
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east4-gcp"
                    )
                )
                print(f"✅ Index created: {settings.PINECONE_INDEX_NAME}")
            
            self.vector_store = PineconeVectorStore(
                index_name=settings.PINECONE_INDEX_NAME,
                embedding=self.embeddings,
                pinecone_api_key=PINECONE_API_KEY
            )
            print("✅ Pinecone connected successfully!")
            
        except Exception as e:
            print(f"❌ Pinecone error: {e}")
            raise
    
    def process_pdf(self, file_path: str) -> int:
        print(f"📄 Processing: {file_path}")
        
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        chunks = self.text_splitter.split_documents(documents)
        
        for chunk in chunks:
            chunk.metadata["source"] = os.path.basename(file_path)
            chunk.metadata["timestamp"] = time.time()
        
        self.vector_store.add_documents(chunks)
        self.total_chunks += len(chunks)
        
        print(f"✅ Added {len(chunks)} chunks")
        return len(chunks)
    
    def get_total_chunks(self) -> int:
        return self.total_chunks