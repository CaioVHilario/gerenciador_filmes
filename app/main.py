from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from .models import Movie
from .database import create_db_and_tables, get_session
from .schemas import MovieCreate, MovieUpdate, MovieResponse

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

#CREATE - Cria um novo filme no banco de dados
@app.post("/movies/", response_model=Movie)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie(**movie.model_dump())

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie

# READ ALL - Busca todos os filmes
@app.get("/movies/", response_model=list[Movie])
def read_all_movies(session: Session = Depends(get_session)):
    statement = select(Movie)
    results = session.exec(statement)
    movies = results.all()

    return movies


#READ ONE - Busca filme por ID
@app.get("/movies/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)

    if not movie:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found."
        )
    
    return movie

#UPDATE - Atualiza campos do objeto existente (parcial)
@app.patch("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    session: Session = Depends(get_session)
):
    db_movie = session.get(Movie, movie_id)

    if not db_movie:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Movie with ID {movie_id} not found."
        )

    update_data = movie_update.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"No fields provided for the update."
        )
    
    for Field, value in update_data.items():
        setattr(db_movie, Field, value)
    
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie

#DELETE - Deleta um filme
@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    session: Session = Depends(get_session)
):
    db_movie = session.get(Movie, movie_id)

    if not db_movie:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Movie with ID {movie_id} not found."
        )
    
    session.delete(db_movie)
    session.commit()

    return{
        "message": f"Movie {db_movie.title} (ID: {movie_id}), successfully deleted.",
        "deleted_movie": {
            "id": movie_id,
            "title": db_movie.title,
            "director": db_movie.director
        }
    }