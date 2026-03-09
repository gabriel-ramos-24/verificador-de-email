import os
import smtplib
from random import randint
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")
JWT_SECRET = os.getenv("JWT_SECRET")

if not EMAIL_REMETENTE or not EMAIL_SENHA_APP or not JWT_SECRET:
    raise RuntimeError("As variáveis de ambiente obrigatórias não foram configuradas.")

app = FastAPI()


class EmailRequest(BaseModel):
    email: EmailStr


class Verificador(BaseModel):
    token: str
    code: int


def enviar_email(destinatario: str, codigo_verificador: int):
    email = EmailMessage()
    email["Subject"] = "Verificação de Email"
    email["From"] = EMAIL_REMETENTE
    email["To"] = destinatario
    email.set_content(f"O seu código é: {codigo_verificador}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMETENTE, EMAIL_SENHA_APP)
        smtp.send_message(email)


@app.post("/enviar-email/")
def enviar(dados: EmailRequest):
    payload = {
        "email": str(dados.email),
        "code": randint(1000, 9999),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=1)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    enviar_email(payload["email"], payload["code"])

    return {
        "token": token,
        "mensagem": "E-mail enviado com sucesso."
    }


@app.post("/verificar-email/")
def verificar(obj: Verificador):
    try:
        dados = jwt.decode(obj.token, JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    if dados["code"] != obj.code:
        raise HTTPException(status_code=401, detail="Código incorreto.")

    return {"mensagem": "Login realizado com sucesso!"}