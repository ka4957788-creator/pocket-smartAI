from fastapi import APIRouter,Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..auth import optional_user
r=APIRouter();t=Jinja2Templates('app/templates')
def render(req,name,**kw):return t.TemplateResponse(req,name,{'user':optional_user(req),**kw})
@r.get('/')
def home(req:Request):return render(req,'index.html')
@r.get('/register')
def reg(req:Request):return render(req,'register.html')
@r.get('/login')
def login(req:Request):return render(req,'login.html')
def protected(req,name):
    if not optional_user(req):return RedirectResponse('/login',303)
    return render(req,name)
@r.get('/dashboard')
def dashboard(req:Request):return protected(req,'dashboard.html')
@r.get('/home-planner')
def hp(req:Request):return protected(req,'home_planner.html')
@r.get('/party-planner')
def pp(req:Request):return protected(req,'party_planner.html')
@r.get('/jewelry-planner')
def jp(req:Request):return protected(req,'jewelry_planner.html')
@r.get('/history')
def hist(req:Request):return protected(req,'history.html')
@r.get('/session-info')
def session(req:Request):
    u=optional_user(req);return {'logged_in':bool(u),'user':u}
@r.get('/session-data')
def session_data(req:Request):return {'user':optional_user(req)}
@r.get('/recommendations-details')
def details():return {'message':'Use /api/history for saved recommendation details.'}
@r.get('/startup')
def startup():return {'status':'ready'}
