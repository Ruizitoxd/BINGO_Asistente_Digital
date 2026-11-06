import hashlib, hmac, secrets
from app.core.config import get_settings

def issue_token() -> str:
    return secrets.token_urlsafe(40)

def hash_token(token: str) -> str:
    pepper = get_settings().token_pepper.encode()
    return hmac.new(pepper, token.encode(), hashlib.sha256).hexdigest()

def verify_token(token: str, expected_hash: str) -> bool:
    return hmac.compare_digest(hash_token(token), expected_hash)
