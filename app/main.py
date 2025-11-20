from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from .routers.movies import router as movies_router
from .routers.auth import router as auth_router
from .database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Função que será executada anets do app inciar, 
    e depois que o app desligar"""
    print("Inciando a API e criando o banco de dados...")
    create_db_and_tables()
    yield
    print("Desligando a API...")

app = FastAPI(
    lifespan=lifespan,
    title="API de Gerenciador de Lista de Filmes",
    version="1.0.0"
)

app.include_router(movies_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Gerenciador de Lista de Filmes!"}