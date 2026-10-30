from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Cria o arquivo do banco de dados chamado "klstore.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./klstore.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para a API usar o banco de dados a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()