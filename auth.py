from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Configuração para criptografar senhas (usando bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chave secreta da nossa API (num projeto real, isto fica escondido)
SECRET_KEY = "klstore_chave_super_secreta_para_tokens"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # O token expira em 30 min

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt