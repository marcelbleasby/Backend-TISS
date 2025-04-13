# backend/app/core/auth.py
from fastapi import Request, HTTPException

STATIC_TOKEN = "TESTE"

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação ausente ou inválido.")
    token = auth_header.split("Bearer ")[1]
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido.")
