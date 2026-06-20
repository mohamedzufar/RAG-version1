# rag-production

A sample retrieval-augmented generation service built with FastAPI.

## Structure

- `app/main.py` - FastAPI app and endpoints
- `app/config.py` - configuration and settings
- `app/models.py` - Pydantic schemas
- `app/rag/` - ingestion, retrieval, generation, evaluation
- `app/cache/redis_client.py` - Redis cache client
- `app/utils/` - fallback and metrics utilities
- `data/` - storage for PDFs
- `scripts/` - population and evaluation scripts
- `tests/` - unit tests

## Run locally

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Test evaluation:
   ```bash
   python scripts/evaluate.py
   ```
