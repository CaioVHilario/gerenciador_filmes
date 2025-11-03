from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from .models import Movie
from .routers import movies
from .database import create_db_and_tables, get_session

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

app.include_router(movies.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Gerenciador de Lista de Filmes!"}

#Lista todos os filmes na URL /movies/
@app.get("/movies/")
def read_Movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    return movies