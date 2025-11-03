from sqlmodel import Session, select
from fastapi import Depends, APIRouter, status, HTTPException, Query

from ..database import get_session
from ..schemas import MovieCreate, MovieResponse, MovieUpdate
from ..models import Movie

router = APIRouter(prefix="/movies", tags=["movies"])

#CRUD BÁSICO

#-------------------------------------------------------------------------------

#CREATE - Cria um novo filme no banco de dados
@router.post("/", response_model=Movie)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie(**movie.model_dump())

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie

# READ ALL - Busca todos os filmes
@router.get("/", response_model=list[Movie])
def read_all_movies(session: Session = Depends(get_session)):
    statement = select(Movie)
    results = session.exec(statement)
    movies = results.all()

    return movies


#READ ONE - Busca filme por ID
@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)

    if not movie:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found."
        )
    
    return movie

#UPDATE - Atualiza campos do objeto existente (parcial)
@router.patch("/{movie_id}", response_model=MovieResponse)
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
@router.delete("/{movie_id}")
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

#-------------------------------------------------------------------------------

#BUSCA AVANÇADA

#READ ONE - Busca por filme pelo título do filme
@router.get("/search/title/advanced", response_model=list[Movie])
def read_movie_by_title(
    q: str = Query(..., min_lenght = 1, description="Termo de busca no título"),
    exact_match: bool = Query(False, description="Busca exata (vs parcial)"),
    sort_by: str = Query("title", description="Como ordenar: title, year, rating"),
    sort_order: str = Query("asc", description="Direção: asc ou desc"),
    session: Session = Depends(get_session)
    ):

    statement = select(Movie)

    if exact_match:
        statement = statement.where(Movie.title == q)
    else:
        search_term = f"%{q}%"
        statement = statement.where(Movie.title.ilike(search_term))
    
    if sort_by == "year":
        order_field = Movie.year
    elif sort_by == "rating":
        order_field = Movie.rating
    else:
        order_field = Movie.title

    if sort_order == "desc":
        statement = statement.order_by(order_field.desc())
    else:
        statement = statement.order_by(order_field.asc())

    results = session.exec(statement)
    movies = results.all()
    return movies

#READ OE - Busca por filme pelo nome do diretor
@router.get("/search/director/advanced", response_model=list[Movie])
def read_movie_by_director(
    q: str = Query(..., min_length=1, description="Termo de busca do diretor"),
    exact_match: bool = Query(False, description="Busca exata (vs parcial)"),
    sort_by: str = Query("title", description="Como ordenar: title, year ou rating"),
    sort_order: str = Query("asc", description="Direção: asc ou desc"),
    session: Session = Depends(get_session)
):
    
    statement = select(Movie)

    if exact_match:
        statement = statement.where(Movie.director == q)
    else:
        search_term = f"%{q}%"
        statement = statement.where(Movie.director.ilike(search_term))
    
    if sort_by == "year":
        order_field = Movie.year
    elif sort_by == "ratting":
        order_field = Movie.rating
    else:
        order_field = Movie.title
    
    if sort_order == "desc":
        statement = statement.order_by(order_field.desc())
    else:
        statement = statement.order_by(order_field.desc())
    
    results = session.exec(statement)
    movie = results.all()
    return movie

