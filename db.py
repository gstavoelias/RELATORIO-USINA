"""
Objetos do sqlalchemy core para a realização da conexão e operação do Banco de Dados
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_CONNECTION = URL.create(
    drivername="postgresql",
    username="postgres",
    password="1234",
    host="10.8.0.13",
    port=5432,
    database="stemis"
)
engine = create_engine(DB_CONNECTION, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)