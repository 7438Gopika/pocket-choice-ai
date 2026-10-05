from fastapi import Depends,HTTPException,Request
from sqlalchemy.orm import Session
from app.auth import decode_access_token
from app.database import get_db
from app.models import User

def get_current_user(request:Request,db:Session=Depends(get_db)):
    uid=request.session.get("user_id")
    if uid: 
        u=db.get(User,int(uid))
        if u:return u
    h=request.headers.get("Authorization","")
    if h.lower().startswith("bearer "):
        u=db.get(User,int(decode_access_token(h.split(" ",1)[1])))
        if u:return u
    raise HTTPException(401,"Login required")
def optional_current_user(request,db=Depends(get_db)):
    try:return get_current_user(request,db)
    except HTTPException:return None
