# etf_ingest_service

Start:
1. Set .env DATABASE_URL
2. poetry install
3. alembic upgrade head
4. uvicorn app.main:app --reload
