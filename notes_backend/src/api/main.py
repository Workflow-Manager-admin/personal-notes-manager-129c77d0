from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.notes_api import router as notes_router

app = FastAPI(
    title="Personal Notes Manager API",
    description="API backend for managing personal notes.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint for the Notes backend"""
    return {"message": "Healthy"}

# Register the notes API router
app.include_router(notes_router)
