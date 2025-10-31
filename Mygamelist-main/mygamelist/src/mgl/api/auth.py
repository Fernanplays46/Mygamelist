from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str

def get_current_user() -> Optional[User]:
    # Stub sin seguridad real: siempre devuelve un usuario "demo"
    return User(username="demo")
