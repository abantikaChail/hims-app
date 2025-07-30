from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app.database import engine
from app.models import Base
from app.routes import router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def root():
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)

