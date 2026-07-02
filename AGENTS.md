# SmartMinutes - Security Utilities
# Responsibilities: Password hashing, verification, and JWT authentication management.

import os
from datetime import datetime, timedelta
from typing import Optional, Union, Any
# In a real environment, you would use:
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# Fake Secret Key and Configurations
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key-for-local-dev-smart-minutes-129837")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# In a real app, instantiate the CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a plain password matches its stored bcrypt hash"""
    # Real logic: return pwd_context.verify(plain_password, hashed_password)
    # Simple mockup verification:
    return hashed_password == f"hashed_{plain_password}"

def get_password_hash(password: str) -> str:
    """Generates a bcrypt hash of a plain password"""
    # Real logic: return pwd_context.hash(password)
    # Simple mockup hashing:
    return f"hashed_{password}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token containing the user id or email"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Real logic:
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return encoded_jwt
    
    # Mock token creation
    mock_jwt = f"mock-jwt-header.payload-{to_encode['sub']}-expires-{expire.timestamp()}.signature"
    return mock_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decodes a JWT token to verify its validity and return its payload"""
    try:
        # Real logic:
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # return payload
        
        # Mock token decoding
        if token.startswith("mock-jwt-"):
            parts = token.split("-")
            sub = parts[2]
            return {"sub": sub}
        return None
    except Exception:
        return None
