# backend/app/services/docling_service.py
import subprocess
import tempfile
import json
import os
from app.models import Guide
from app.database import SessionLocal
from datetime import datetime

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
 

def build_tiss_payload(guide_type, patient, provider, operator, procedimentos):
    return {
        "cabecalho": {
            "identificacaoTransacao": {
                "tipoTransacao": "ENVIO",
                "sequencialTransacao": "0001"
            },
            "dataRegistroTransacao": datetime.now().strftime("%Y-%m-%d"),
            "horaRegistroTransacao": datetime.now().strftime("%H:%M:%S")
        },
        "identificacaoPrestador": {
            "cnpjPrestador": provider["cnpj"],
            "nomePrestador": provider["nome"]
        },
        "guia": {
            "tipo": guide_type,
            "numeroGuiaPrestador": "123456789",
            "dadosBeneficiario": {
                "nomeBeneficiario": patient["nome"],
                "numeroCarteira": patient["carteira"]
            },
            "dadosContratadoExecutante": {
                "cnpjContratado": provider["cnpj"],
                "nomeContratado": provider["nome"]
            },
            "procedimentos": procedimentos
        },
        "operadora": {
            "registroANS": operator["registro_ans"],
            "nomeOperadora": operator["nome"]
        }
    }

def gerar_e_salvar_guia(guide_type, patient, provider, operator, procedimentos, db):
    data = build_tiss_payload(guide_type, patient, provider, operator, procedimentos)
    xml = generate_tiss_xml(data)
    guia = Guide(
        guide_type=guide_type,
        patient_name=patient["nome"],
        provider_name=provider["nome"],
        operator_name=operator["nome"],
        xml_content=xml
    )
    db.add(guia)
    db.commit()
    db.refresh(guia)
    return guia