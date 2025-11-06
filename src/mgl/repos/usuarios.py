from sqlmodel import Session, select
from passlib.context import CryptContext
from mgl.domain.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # bcrypt no admite contraseñas de más de 72 bytes
    return pwd_context.hash(password[:72])


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_user(session: Session, username: str, password: str):
    hashed = hash_password(password)
    user = User(username=username, password_hash=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, username: str):
    query = select(User).where(User.username == username)
    return session.exec(query).first()
