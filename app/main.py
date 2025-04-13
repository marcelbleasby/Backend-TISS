from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.api import guides

app = FastAPI(title="TISS Backend", description="Backend API for TISS application")

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(guides.router, prefix="/guides", tags=["Guides"])

@app.get("/")
def root():
    return {"message": "TISS Backend rodando!"}
