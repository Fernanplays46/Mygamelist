from mgl.repos.user_repo import get_user, create_user
from mgl.infra.database import get_session
from mgl.repos.user_repo import verify_password

def register_user(session, username, password):
    if get_user(session, username):
        return False, "El usuario ya existe"
    create_user(session, username, password)
    return True, None

def login_user(session, username, password):
    user = get_user(session, username)
    
    if not user or not verify_password(password, user.password_hash):
        return False, "Credenciales incorrectas"
    
    return True, user.username
