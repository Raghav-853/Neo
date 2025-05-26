from fastapi import FastAPI
from app.core.config import settings
from sqlalchemy import text
from app.db.session import engine
from app.api import auth, events

app = FastAPI(
    title="NeoFi Event API",
    description="Backend for collaborative event management",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(events.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def test_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed:", e)