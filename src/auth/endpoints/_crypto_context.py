from passlib.context import CryptContext

SECRET_KEY = "688d78853c72d1e2da3f716d42fe32cb3e10b8fb807b22b7a3dab1fa4ed27e3c"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
