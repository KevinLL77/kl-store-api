from pydantic import BaseModel, Field
from typing import Optional

# --- MOLDES DO UTILIZADOR ---
class UsuarioCreate(BaseModel):
    username: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- MOLDES DA CATEGORIA ---
class CategoriaCreate(BaseModel):
    nome: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

# --- MOLDES DO PRODUTO (COM VALIDAÇÃO E FOTO) ---
class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=2, description="O nome deve ter pelo menos 2 caracteres")
    descricao: Optional[str] = None
    preco: float = Field(..., gt=0, description="O preço deve ser maior que zero")
    quantidade: int = Field(..., ge=0, description="A quantidade não pode ser negativa")
    foto_url: Optional[str] = None
    categoria_id: int

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int
    foto_url: Optional[str] = None
    categoria_id: int

    class Config:
        from_attributes = True