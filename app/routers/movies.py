from sqlmodel import Session, select
from fastapi import Depends, APIRouter, status, HTTPException, Query
from typing import Optional
from math import ceil

import sqlmodel

from ..database import get_session
from ..schemas import MovieCreate, MovieResponse, MovieUpdate, PaginatedResponse
from ..models import Movie

router = APIRouter(prefix="/movies", tags=["movies"])

#Funções para paginação

#-------------------------------------------------------------------------------

def apply_pagination(statement, page: int, page_size: int):

    #Evita erros de passar numeração de pagina 0 ou negativa
    if page < 1:
        page = 1
    
    #calcula quantos itens devem ser pulados para eexibir somente os correspondes da pagina
    skip = (page - 1) * page_size   
    return statement.offset(skip).limit(page_size)

def calcule_pagination_metadata(
        total_itens: int, 
        page: int, 
        page_size: int
        ) -> dict:
    
    #calcula o número de paginas arredondando pra cima a divisão dos itens pelo tamanho da pagina
    total_pages = ceil(total_itens/page_size) if total_itens > 0 else 1

    return {
        "total": total_itens,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


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

# READ ALL - Busca todos os filmes com paginação
@router.get("/", response_model=PaginatedResponse[Movie])
def read_all_movies(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Número de itens por página"),
    session: Session = Depends(get_session)
    ):
    count_statement = select(sqlmodel.func.count(Movie.id))
    total_movies = session.exec(count_statement).one()

    if isinstance(total_movies, tuple):
        total_movies = total_movies[0]

    statement = select(Movie)
    statement = apply_pagination(statement, page, page_size)

    results = session.exec(statement)
    movies = results.all()

    pagination_meta = calcule_pagination_metadata(total_movies, page, page_size)

    return PaginatedResponse(
        data=movies,
        **pagination_meta
    )

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

#READ - Busca por filme pelo título do filme
@router.get("/search/title/advanced", response_model=PaginatedResponse[Movie])
def read_movie_by_title(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Número de itens por página"),
    q: str = Query(..., min_lenght = 1, description="Termo de busca no título"),
    exact_match: bool = Query(False, description="Busca exata (vs parcial)"),
    sort_by: str = Query("title", description="Como ordenar: title, year, rating"),
    sort_order: str = Query("asc", description="Direção: asc ou desc"),
    session: Session = Depends(get_session)
    ):

    statement = select(Movie)
    count_statement = select(sqlmodel.func.count(Movie.id))

    if exact_match:
        statement = statement.where(Movie.title == q)
        count_statement = count_statement.where(Movie.title == q)
    else:
        search_term = f"%{q}%"
        statement = statement.where(Movie.title.ilike(search_term))
        count_statement = count_statement.where(Movie.title.ilike(search_term))
    
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

    statement = apply_pagination(statement, page, page_size)

    results = session.exec(statement)
    movies = results.all()

    total_movies = session.exec(count_statement).one()

    pagination_meta = calcule_pagination_metadata(total_movies, page, page_size)

    return PaginatedResponse(
        data=movies,
        **pagination_meta
    )

#READ - Busca por filme pelo nome do diretor
@router.get("/search/director/advanced", response_model=PaginatedResponse[Movie])
def read_movie_by_director(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Número de itens por página"),
    q: str = Query(..., min_length=1, description="Termo de busca do diretor"),
    exact_match: bool = Query(False, description="Busca exata (vs parcial)"),
    sort_by: str = Query("title", description="Como ordenar: title, year ou rating"),
    sort_order: str = Query("asc", description="Direção: asc ou desc"),
    session: Session = Depends(get_session)
):
    
    statement = select(Movie)
    count_statement = select(sqlmodel.func.count(Movie.id))

    if exact_match:
        statement = statement.where(Movie.director == q)
        count_statement = count_statement.where(Movie.director == q)
    else:
        search_term = f"%{q}%"
        statement = statement.where(Movie.director.ilike(search_term))
        count_statement = count_statement.where(Movie.director.ilike(search_term))
    
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
    
    statement = apply_pagination(statement, page, page_size)

    results = session.exec(statement)
    movie = results.all()

    total_movies = session.exec(count_statement).one()

    pagination_meta = calcule_pagination_metadata(total_movies, page, page_size)

    return PaginatedResponse(
        data=movie,
        **pagination_meta
    )

#READ - Busca por filmes por gênero
@router.get("/search/genre/advanced", response_model=PaginatedResponse[Movie])
def read_movies_by_genre(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Número de itens por página"),
    q: str = Query(..., min_length=1, description="Termo de busca do gênero"),
    exact_match: bool = Query(False, description="Busca exata (vs parcial)"),
    sort_by = Query("Title", description="Como ordenar: title, year ou rating"),
    sort_order = Query("asc", description="Direção: asc ou desc"),
    session: Session = Depends(get_session)
):
    statement = select(Movie)
    count_statement = select(sqlmodel.func.count(Movie.id))

    if exact_match:
        statement = statement.where(Movie.genre == q)
        count_statement = count_statement.where(Movie.genre == q)
    else:
        search_term = f"%{q}%"
        statement = statement.where(Movie.genre.ilike(search_term))
        count_statement = count_statement.where(Movie.genre.ilike(search_term))

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

    statement = apply_pagination(statement, page, page_size)

    results = session.exec(statement)
    movie = results.all()

    total_movies = session.exec(count_statement).one()

    pagination_meta = calcule_pagination_metadata(total_movies, page, page_size)

    return PaginatedResponse(
        data=movie,
        **pagination_meta
    )

#READ - Busca filmes com filtros, ordenação e paginação
@router.get("/search/filters/advanced", response_model=PaginatedResponse[Movie])
def search_movies_with_filters_advanced(
    page: int = Query(1, ge=1, description="Pagina atual"),
    page_size: int = Query(20, ge=1, le=100, description="Número de itens por página"),
    title: Optional[str] = Query(None, description="Filtrar por título (parcial)"),
    min_year: Optional[int] = Query(None, ge=1888, le=2100, description="Ano mínimo"),
    max_year: Optional[int] = Query(None, ge=1888, le=2100, description="Ano máximo"),
    director: Optional[str] = Query(None, description="Filtrar por diretor (parcial)"),
    min_rating: Optional[int] = Query(None, ge=1, le=5, description="Avaliação mínima"),
    max_rating: Optional[int] = Query(None, ge=1, le=5, description="Avaliação máxima"),
    genre: Optional[str] = Query(None, description="Filtrar por gênero (parcial)"),
    sort_by: str = Query("title", description="Campo para ordenar: year ou rating"),
    sort_order: str = Query("asc", description="Direção: asc ou desc"),
    skip: int = Query(0, ge=0, description="Número de rgistros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    session: Session = Depends(get_session)
):
    
    filters_provided = any([
        title is not None,
        director is not None,
        genre is not None,
        min_year is not None,
        max_year is not None,
        min_rating is not None,
        max_rating is not None
    ])
    
    if not filters_provided:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Pelo menos um filtro deve ser fornecido (title, director, " \
            "genre, min_year, max_year, min_rating, max_rating)"
        )

    statement = select(Movie)
    count_statement = select(sqlmodel.func.count(Movie.id))

    if title:
        statement = statement.where(Movie.title.ilike(f"%{title}%"))
        count_statement = count_statement.where(Movie.title.ilike(f"%{title}%"))
    if director:
        statement = statement.where(Movie.director.ilike(f"%{director}%"))
        count_statement = count_statement.where(Movie.director.ilike(f"%{director}%"))
    if genre:
        statement = statement.where(Movie.genre.ilike(f"%{genre}%"))
        count_statement = count_statement.where(Movie.genre.ilike(f"%{genre}%"))
    if min_year:
        statement = statement.where(Movie.year >= min_year)
        count_statement = count_statement.where(Movie.year >= min_year)
    if max_year:
        statement = statement.where(Movie.year <= max_year)
        count_statement = count_statement.where(Movie.year <= max_year)
    if min_rating:
        statement = statement.where(Movie.rating >= min_rating)
        count_statement = count_statement.where(Movie.rating >= min_rating)
    if max_rating:
        statement = statement.where(Movie.rating <= max_rating)
        count_statement = count_statement.where(Movie.rating <= max_rating)

    total_movies = session.exec(count_statement).one()

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
    
    statement = apply_pagination(statement, page, page_size)

    results = session.exec(statement)
    movies = results.all()

    pagination_meta = calcule_pagination_metadata(total_movies, page, page_size)

    # return movies

    return PaginatedResponse(
        data=movies,
        **pagination_meta
    )

#READ - Busca em tempo real (typeahead/search-as-you-type)
@router.get("/search/instant", response_model=list[Movie])
def instant_search(
    q: str = Query(..., description=""),
    limit: int = Query(8, ge=1, le=20, description=""),
    session: Session = Depends(get_session)
):
    
    if not q or len(q.strip()) == 0:
        return []
    
    search_term = f"%{q.strip()}%"

    # Busca em multiplos campos com ordenação por relevância
    statement = (
        select(Movie)
        .where(
            (Movie.title.ilike(search_term)) |
            (Movie.director.ilike(search_term)) |
            (Movie.genre.ilike(search_term))
        )
        .order_by(
            #Filmes que o título começa com o termo de busca
            Movie.title.startswith(q.strip()).desc(),
            #Filmes mais populares (mais bem avaliados)
            Movie.rating.desc(),
            #Por fim, em ordem alfabetica
            Movie.title.asc()
        )
        .limit(limit)
    )

    results = session.exec(statement)
    movies = results.all()

    return movies