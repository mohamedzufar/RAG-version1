#!/usr/bin/env python
"""
Bulk upload documents to reach ~1200 chunks
"""
import os
import sys
import requests
from pathlib import Path

API_URL = "http://localhost:8000"
DATA_DIR = "data"

def upload_documents():
    """Upload all PDFs in data directory"""
    pdf_files = list(Path(DATA_DIR).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDFs found in {DATA_DIR}")
        print("Place your PDF files in the data/ directory")
        sys.exit(1)
    
    total_chunks = 0
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    for pdf_path in pdf_files:
        print(f"📤 Uploading: {pdf_path.name}")
        
        with open(pdf_path, "rb") as f:
            files = {"file": (pdf_path.name, f, "application/pdf")}
            response = requests.post(f"{API_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            total_chunks += data["chunk_count"]
            print(f"✅ {pdf_path.name}: {data['chunk_count']} chunks")
        else:
            print(f"❌ {pdf_path.name}: {response.text}")
    
    print(f"\n📊 Total chunks: {total_chunks}")
    print(f"🎯 Target: ~1200 chunks")
    
    if total_chunks >= 1200:
        print("✅ Target reached!")
    else:
        print(f"⚠️ Need {1200 - total_chunks} more chunks. Add more PDFs.")

if __name__ == "__main__":
    upload_documents()