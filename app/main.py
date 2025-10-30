from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from .models import Movie
from .database import create_db_and_tables, get_session
from .schemas import MovieCreate

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

#Lista todos os filmes na URL /movies/
@app.get("/movies/")
def read_Movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    return movies

# CRUD Básico

#-------------------------------------------------------------------------------

#Cria um novo filme no banco de dados
@app.post("/movies/", response_model=Movie)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie(**movie.model_dump())

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie

#Busca todos os filmes
@app.get("/movies/", response_model=list[Movie])
def read_all_movies(session: Session = Depends(get_session)):
    statement = select(Movie)
    results = session.exec(statement)
    movies = results.all()

    return movies


#Busca filme por ID
@app.get("/movies/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)

    if not movie:
        raise HTTPException(
            status_code = 404,
            detail=f"Movie with ID {movie_id} not found."
        )
    
    return movie



# Buscas Específicas

#-------------------------------------------------------------------------------



# Buscas Avançadas

#-------------------------------------------------------------------------------