from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    senha_criptografada = Column(String)

# --- A NOSSA NOVA TABELA DE CATEGORIAS ---
class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)

    # O lado de cá do "fio invisível"
    produtos = relationship("Produto", back_populates="categoria")

# --- A NOSSA TABELA DE PRODUTOS ATUALIZADA ---
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    
    # A Chave Estrangeira (diz a qual categoria o produto pertence)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    # O lado de lá do "fio invisível"
    categoria = relationship("Categoria", back_populates="produtos")
    class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, nullable=True)
    preco = Column(Float)
    quantidade = Column(Integer)
    foto_url = Column(String, nullable=True)  # <-- NOVO
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="produtos")