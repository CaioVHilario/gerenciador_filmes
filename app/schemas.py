from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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