from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import models, schemas, auth
from database import engine, get_db

# Cria tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Gestão KL STORE - Completa")

# --- LIBERA O ACESSO PARA O FRONTEND (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que qualquer página web acesse a API
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# Cadeado visual do Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def raiz():
    return {"mensagem": "API da KL STORE está online e a todo vapor!"}

# ==========================================
# --- ROTAS DE SEGURANÇA (UTILIZADORES) ---
# ==========================================
@app.post("/registrar/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.username == usuario.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username já registado")
    
    senha_hash = auth.get_password_hash(usuario.senha)
    novo_usuario = models.Usuario(username=usuario.username, senha_criptografada=senha_hash)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/token", response_model=schemas.Token)
def login_para_obter_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.username == form_data.username).first()
    if not usuario or not auth.verify_password(form_data.password, usuario.senha_criptografada):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de utilizador ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": usuario.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ==========================================
# --- ROTAS DE CATEGORIAS ---
# ==========================================
@app.post("/categorias/", response_model=schemas.CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    nova_categoria = models.Categoria(nome=categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

@app.get("/categorias/", response_model=list[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db.query(models.Categoria).all()

@app.get("/categorias/{categoria_id}/produtos/", response_model=list[schemas.ProdutoResponse])
def listar_produtos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    produtos = db.query(models.Produto).filter(models.Produto.categoria_id == categoria_id).all()
    return produtos

# ==========================================
# --- ROTAS DE PRODUTOS (COM CRUD COMPLETO) ---
# ==========================================
@app.post("/produtos/", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == produto.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Esta categoria não existe!")

    novo_produto = models.Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        quantidade=produto.quantidade,
        categoria_id=produto.categoria_id
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.get("/produtos/", response_model=list[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db.query(models.Produto).all()

@app.put("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, produto_atualizado: schemas.ProdutoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado nas prateleiras")
    
    produto.nome = produto_atualizado.nome
    produto.descricao = produto_atualizado.descricao
    produto.preco = produto_atualizado.preco
    produto.quantidade = produto_atualizado.quantidade
    produto.categoria_id = produto_atualizado.categoria_id
    
    db.commit()
    db.refresh(produto)
    return produto

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado nas prateleiras")
    
    db.delete(produto)
    db.commit()
    return {"mensagem": f"Produto {produto_id} apagado com sucesso do estoque!"}