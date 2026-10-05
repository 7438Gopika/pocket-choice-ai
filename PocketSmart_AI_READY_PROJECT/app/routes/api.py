import json
from pathlib import Path
from fastapi import APIRouter,Depends,File,Form,HTTPException,Request,UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth import create_access_token,hash_password,verify_password
from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User,Recommendation
from app.schemas import HomeRequest,PartyRequest,JewelryRequest,RecommendationResponse
from app.services.catalog import search_catalog
from app.services.gemini_utils import safe_home,safe_party,safe_jewelry
r=APIRouter(); s=get_settings(); Path("uploads").mkdir(exist_ok=True)
def save(db,u,planner,req,res):
    x=Recommendation(user_id=u.id,planner=planner,title=res.title,request_json=json.dumps(req,ensure_ascii=False),response_json=res.model_dump_json());db.add(x);db.commit();db.refresh(x);return x
@r.post("/register")
def register(p:dict,request:Request,db:Session=Depends(get_db)):
    email=str(p.get("email","")).strip().lower(); password=str(p.get("password","")); name=str(p.get("full_name","")).strip()
    if "@" not in email:raise HTTPException(422,"Enter a valid email.")
    if len(password)<8:raise HTTPException(422,"Password must be at least 8 characters.")
    if not name:raise HTTPException(422,"Full name is required.")
    if db.query(User).filter(User.email==email).first():raise HTTPException(409,"An account with this email already exists.")
    u=User(email=email,full_name=name,password_hash=hash_password(password));db.add(u);db.commit();db.refresh(u);request.session["user_id"]=u.id
    return {"message":"Registration successful","user":{"id":u.id,"email":u.email,"full_name":u.full_name}}
@r.post("/login")
def login(p:dict,request:Request,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==str(p.get("email","")).strip().lower()).first()
    if not u or not verify_password(str(p.get("password","")),u.password_hash):raise HTTPException(401,"Incorrect email or password.")
    request.session["user_id"]=u.id;return {"message":"Login successful"}
@r.post("/logout")
def logout(request):request.session.clear();return {"message":"Logged out"}
@r.post("/token")
def token(f:OAuth2PasswordRequestForm=Depends(),db=Depends(get_db)):
    u=db.query(User).filter(User.email==f.username.lower()).first()
    if not u or not verify_password(f.password,u.password_hash):raise HTTPException(401,"Incorrect email or password.")
    return {"access_token":create_access_token(u.id),"token_type":"bearer"}
@r.get("/session-info")
def session_info(u=Depends(get_current_user)):return {"authenticated":True,"user_id":u.id,"email":u.email,"full_name":u.full_name}
@r.get("/session-data")
def session_data(u=Depends(get_current_user),db=Depends(get_db)):return {"user_id":u.id,"recommendation_count":db.query(Recommendation).filter(Recommendation.user_id==u.id).count()}
@r.post("/generate-home",response_model=RecommendationResponse)
def generate_home(p:HomeRequest,u=Depends(get_current_user),db=Depends(get_db)):
    res=safe_home(p,search_catalog("home",p.budget,[x.name for x in p.items]));save(db,u,"home",p.model_dump(),res);return res
@r.post("/generate-party",response_model=RecommendationResponse)
def generate_party(p:PartyRequest,u=Depends(get_current_user),db=Depends(get_db)):
    res=safe_party(p,search_catalog("party",p.budget));save(db,u,"party",p.model_dump(),res);return res
@r.post("/generate-jewelry",response_model=RecommendationResponse)
async def generate_jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("elegant"),metal_preference:str=Form("any"),notes:str=Form(""),outfit_image:UploadFile|None=File(None),u=Depends(get_current_user),db=Depends(get_db)):
    image=mime=None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}:raise HTTPException(415,"Only JPG, PNG and WEBP images are supported.")
        image=await outfit_image.read()
        if len(image)>s.max_image_mb*1024*1024:raise HTTPException(413,f"Image must be <= {s.max_image_mb} MB.")
        mime=outfit_image.content_type
    p=JewelryRequest(budget=budget,occasion=occasion,style=style,metal_preference=metal_preference,notes=notes);res=safe_jewelry(p,search_catalog("jewelry",budget),image,mime);save(db,u,"jewelry",p.model_dump(),res);return res
@r.get("/recommendations-details/{rid}")
def details(rid:int,u=Depends(get_current_user),db=Depends(get_db)):
    x=db.get(Recommendation,rid)
    if not x or x.user_id!=u.id:raise HTTPException(404,"Recommendation not found.")
    return {"id":x.id,"planner":x.planner,"title":x.title,"created_at":x.created_at,"request":json.loads(x.request_json),"response":json.loads(x.response_json)}
@r.get("/history")
def history(u=Depends(get_current_user),db=Depends(get_db)):
    return [{"id":x.id,"planner":x.planner,"title":x.title,"created_at":x.created_at} for x in db.query(Recommendation).filter(Recommendation.user_id==u.id).order_by(Recommendation.created_at.desc()).all()]
@r.get("/health")
def health():return {"status":"ok","service":"PocketSmart AI"}
