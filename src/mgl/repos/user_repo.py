from sqlmodel import select
from mgl.domain.user import User
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(password, hashed)

def get_user(session, username: str):
    return session.exec(
        select(User).where(User.username == username)
    ).first()

def create_user(session, username: str, password: str):
    user = User(username=username, password_hash=hash_password(password))
    session.add(user)
    session.commit()
