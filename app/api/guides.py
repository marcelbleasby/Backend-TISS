# backend/app/api/guides.py
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Literal, List, Optional
from sqlalchemy.orm import Session
from app.services.docling_service import generate_tiss_xml
from app.database import get_db
from app.models import Guide
from app.services.docling_service import gerar_e_salvar_guia

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

class AutoGuideInput(BaseModel):
    guide_type: Literal["consulta", "sadt", "internacao"]
    patient: dict
    provider: dict
    operator: dict
    procedimentos: List[dict]

@router.post("/auto")
def criar_guia_automatica(payload: AutoGuideInput, db: Session = Depends(get_db)):
    guia = gerar_e_salvar_guia(
        guide_type=payload.guide_type,
        patient=payload.patient,
        provider=payload.provider,
        operator=payload.operator,
        procedimentos=payload.procedimentos,
        db=db
    )
    return {
        "id": guia.id,
        "mensagem": "Guia preenchida e salva com sucesso!"
    }
