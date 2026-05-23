from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine, Base

from app.models.enquiry import Enquiry
from app.models.event import Event
from app.api.enquiry import router as enquiry_router

app = FastAPI(
    title="Closira Backend Assignment",
    description="Customer enquiry handling workflow",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(enquiry_router)

@app.get("/")
def root():
    return {"message": "Closira Backend Running"}


@app.get("/health")
def health_check():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }