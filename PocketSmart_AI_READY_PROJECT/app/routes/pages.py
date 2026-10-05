from fastapi import APIRouter,Depends,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import optional_current_user
r=APIRouter()
def page(request,name,user): return request.app.state.templates.TemplateResponse(name,{"request":request,"user":user})
@r.get("/",response_class=HTMLResponse)
def home(request:Request,db=Depends(get_db)):return page(request,"index.html",optional_current_user(request,db))
@r.get("/register",response_class=HTMLResponse)
def register(request:Request):return page(request,"register.html",None)
@r.get("/login",response_class=HTMLResponse)
def login(request:Request):return page(request,"login.html",None)
def protected(request:Request,db,name):
    u=optional_current_user(request,db)
    return page(request,name,u) if u else RedirectResponse("/login",303)
@r.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request,db=Depends(get_db)):return protected(request,db,"dashboard.html")
@r.get("/planner/home",response_class=HTMLResponse)
def home_planner(request:Request,db=Depends(get_db)):return protected(request,db,"home_planner.html")
@r.get("/planner/party",response_class=HTMLResponse)
def party_planner(request:Request,db=Depends(get_db)):return protected(request,db,"party_planner.html")
@r.get("/planner/jewelry",response_class=HTMLResponse)
def jewelry_planner(request:Request,db=Depends(get_db)):return protected(request,db,"jewelry_planner.html")
@r.get("/history-page",response_class=HTMLResponse)
def history_page(request:Request,db=Depends(get_db)):return protected(request,db,"history.html")
