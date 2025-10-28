# models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Movie(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    
    title: str = Field(index=True) #campo de título do filme obrigatorio
    year: int #campo de ano do filme obrigatorio
    director: str = Field(index=True) #campo de diretor do filme obrigatorio
    genre: Optional[str] = Field(default=None) #campo de genero do filme 
    # rating: Optional[int] = Field(default=None, ge=0, le=5) #campo de avaliação do filme 
    # comment: Optional[str] = Field(default=None) #Breve comentario de opnião do filme