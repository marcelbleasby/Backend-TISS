# backend/app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import guides
from app.core.auth import verify_token
from app.database import Base, engine

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


# backend/app/core/auth.py
from fastapi import Request, HTTPException

STATIC_TOKEN = "seu_token_super_seguro"

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação ausente ou inválido.")
    token = auth_header.split("Bearer ")[1]
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido.")


# backend/app/api/guides.py
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Literal, List, Optional
from sqlalchemy.orm import Session
from app.services.docling_service import generate_tiss_xml
from app.database import get_db
from app.models.guide import Guide

router = APIRouter()

class GuideInput(BaseModel):
    guide_type: Literal["consulta", "sadt", "internacao"]
    patient_name: str
    provider_name: str
    operator_name: str
    data: dict

class GuideOutput(BaseModel):
    id: int
    guide_type: str
    patient_name: str
    provider_name: str
    operator_name: str
    xml_content: str

    class Config:
        orm_mode = True

@router.post("/", response_model=GuideOutput)
def create_guide(guide: GuideInput, db: Session = Depends(get_db)):
    try:
        xml_content = generate_tiss_xml(guide.data)

        db_guide = Guide(
            guide_type=guide.guide_type,
            patient_name=guide.patient_name,
            provider_name=guide.provider_name,
            operator_name=guide.operator_name,
            xml_content=xml_content
        )
        db.add(db_guide)
        db.commit()
        db.refresh(db_guide)

        return db_guide
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar guia TISS: {str(e)}")

@router.get("/", response_model=List[GuideOutput])
def list_guides(patient_name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if patient_name:
        return db.query(Guide).filter(Guide.patient_name.ilike(f"%{patient_name}%")).all()
    return db.query(Guide).all()

@router.get("/{guide_id}", response_model=GuideOutput)
def get_guide_by_id(guide_id: int, db: Session = Depends(get_db)):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Guia não encontrada")
    return guide


# backend/app/services/docling_service.py
import subprocess
import tempfile
import json
import os

def generate_tiss_xml(data: dict) -> str:
    with tempfile.TemporaryDirectory() as tempdir:
        input_path = os.path.join(tempdir, "input.json")
        output_path = os.path.join(tempdir, "output.xml")

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        result = subprocess.run([
            "docling", "render",
            "--input", input_path,
            "--output", output_path,
            "--format", "xml"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Erro no Docling: {result.stderr}")

        with open(output_path, "r", encoding="utf-8") as f:
            return f.read()


# backend/app/models/guide.py
from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Guide(Base):
    __tablename__ = "guides"

    id = Column(Integer, primary_key=True, index=True)
    guide_type = Column(String, index=True)
    patient_name = Column(String, index=True)
    provider_name = Column(String)
    operator_name = Column(String)
    xml_content = Column(Text)


# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/tiss")

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
ESTE ARQUIVO É APENAS UM EXEMPLO DA ESTRUTURA DO BACKEND, LEVEM APENAS COMO BASE
