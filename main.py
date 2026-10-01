from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routers import pages,auth,planners,history
s=get_settings();app=FastAPI(title=s.app_name,version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.mount('/static',StaticFiles(directory='app/static'),name='static')
app.include_router(pages.r);app.include_router(auth.r,prefix='/api');app.include_router(planners.r,prefix='/api');app.include_router(history.r,prefix='/api')
@app.on_event('startup')
def startup():init_db()
@app.get('/health')
def health():return {'status':'ok','service':s.app_name}
