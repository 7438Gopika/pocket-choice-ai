from datetime import datetime,timedelta,timezone
import base64,hashlib,hmac,os
import jwt
from fastapi import HTTPException
from app.config import get_settings
settings=get_settings()

def hash_password(password:str)->str:
    salt=os.urandom(16)
    digest=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
    return base64.urlsafe_b64encode(salt).decode()+":"+base64.urlsafe_b64encode(digest).decode()

def verify_password(password:str,stored:str)->bool:
    try:
        salt_b64,digest_b64=stored.split(":",1)
        salt=base64.urlsafe_b64decode(salt_b64.encode())
        expected=base64.urlsafe_b64decode(digest_b64.encode())
        actual=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
        return hmac.compare_digest(actual,expected)
    except Exception:return False

def create_access_token(sub,minutes=60):
    n=datetime.now(timezone.utc)
    return jwt.encode({"sub":str(sub),"iat":n,"exp":n+timedelta(minutes=minutes)},settings.secret_key,algorithm="HS256")

def decode_access_token(token):
    try:
        p=jwt.decode(token,settings.secret_key,algorithms=["HS256"]); return str(p["sub"])
    except Exception as e: raise HTTPException(401,"Invalid or expired token") from e
