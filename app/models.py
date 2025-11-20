# models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Movie(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    
    title: str = Field(index=True) #campo de título do filme obrigatorio
    year: int = Field(ge=1888, le=datetime.now().year) #campo de ano do filme obrigatorio
    director: str = Field(index=True) #campo de diretor do filme obrigatorio
    genre: Optional[str] = Field(default=None) #campo de genero do filme 
    rating: Optional[int] = Field(default=None, ge=0, le=5) #campo de avaliação do filme 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
    # description: Optional[str] = Field(default=None) #Breve comentario de opnião/descrição do filme

class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)