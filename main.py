from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Field
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

from models import Movie

# Definindo a URL do db
sqlite_file_name = "movies.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    """
    Cria o banco de dados e as tabelas (se não existirem).
    """
    SQLModel.metadata.create_all(engine)

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

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Gerenciador de Lista de Filmes!"}