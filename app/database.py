from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

import os

# definindo o caminho do db (para a pasta data)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

#cria a pasta se não existir
os.makedirs(DATA_DIR, exist_ok=True)

# Definindo a URL do db
sqlite_file_name = "movies.db"
sqlite_url = f"sqlite:///{os.path.join(DATA_DIR, sqlite_file_name)}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    """
    Cria o banco de dados e as tabelas (se não existirem).
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependência para obter a sessão do banco"""
    with Session(engine) as session:
        yield session