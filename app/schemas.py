from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]       #Lista de dados (filmes, usuarios, ...)
    total: int          #Total de registros no db
    page: int           #Número da pagina atual
    page_size: int      #Número de ítens na pagina
    total_pages: int    #Número de paginas
    has_next: bool      #Informa se tem uma pagina depois
    has_prev: bool      #Informa se tem pagina anterior

    class Config:
        from_attributes = True

class MovieCreate(BaseModel):
    title: str
    year: int
    director: str
    rating: int
    genre: str
    description: Optional[str] = None

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    director: Optional[str] = None
    rating: Optional[float] = None
    genre: Optional[str] = None
    description: Optional[str] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    year: int
    director: str
    rating: float
    genre: str
    description: Optional[str] = None
    created_at: datetime
    update_at: datetime 

    class Config:
        from_attributes = True

#-------------------------------------------------------------------------------

#SCHEMAS PARA USUÁRIOS

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None