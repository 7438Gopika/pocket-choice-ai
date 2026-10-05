from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.database import Base,engine
from app.routes.pages import r as page_router
from app.routes.api import r as api_router
s=get_settings(); base=Path(__file__).resolve().parent
@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield

app=FastAPI(title=s.app_name,version="1.0.0",description="Smart budget and recommendation assistant",lifespan=lifespan)
app.add_middleware(SessionMiddleware,secret_key=s.secret_key,session_cookie=s.session_cookie,max_age=s.session_max_age,same_site="lax")
app.add_middleware(CORSMiddleware,allow_origins=s.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory=base/"static"),name="static");app.state.templates=Jinja2Templates(directory=base/"templates")
app.include_router(page_router);app.include_router(api_router)
if __name__=="__main__":
 import uvicorn;uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
