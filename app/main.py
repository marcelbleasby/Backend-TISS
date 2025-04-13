from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import Guide
from app import guides
from app.database import Base, engine, get_db
from app.core.auth import verify_token

app = FastAPI()

# Criar as tabelas
Base.metadata.create_all(bind=engine)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_auth(request: Request, call_next):
    try:
        verify_token(request)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    return await call_next(request)

app.include_router(guides.router, prefix="/guides", tags=["Guides"])

@app.get("/")
def root():
    return {"message": "TISS Backend rodando!"}
