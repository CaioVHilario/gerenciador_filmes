from datetime import datetime, timedelta
import jwt
from jwt import PyJWKError, ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM", "HS256")
ACESS_TOKEN_EXPIRE_MINUTES=os.gentev("ACESS_TOKEN_EXPIRE_MINUTES", "30")

if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY NÃO ENCONTRADA. "
        "Crie um arquivo .env baseado no .env.example e configure a SECRET_KEY."
    )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#Verifica a senha com a senha hasheada para saber se coincidem
def verify_password(plain_passord, hashed_passord):
    return pwd_context.verify(plain_passord, hashed_passord)

#Função para hashear senhas
def get_password_hash(password):
    return pwd_context.hash(password)

#Criar token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Verifica o token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Expired token"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    