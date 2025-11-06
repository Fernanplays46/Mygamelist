"""Simple password hashing utilities using PBKDF2-HMAC (sha256)."""

from __future__ import annotations
import os
import hashlib
import hmac
from typing import Tuple

def hash_password(password: str, iterations: int = 200_000) -> str:
    """Return a string iterations:salt:hashhex"""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{iterations}:{salt.hex()}:{dk.hex()}"

def verify_password(password: str, stored: str) -> bool:
    """Verify a password against stored iterations:salt:hashhex"""
    try:
        iterations_s, salt_hex, hash_hex = stored.split(":")
        iterations = int(iterations_s)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False
