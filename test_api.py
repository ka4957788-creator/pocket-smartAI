import os
os.environ['DATABASE_PATH']='./data/test_pocketsmart.db';os.environ['SECRET_KEY']='test-secret';os.environ['GEMINI_API_KEY']=''
from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_health(): assert c.get('/health').status_code==200
def test_register_login_home():
    e='test@example.com';c.post('/api/register',data={'name':'Test User','email':e,'password':'secret123'});r=c.post('/api/login',data={'email':e,'password':'secret123'},follow_redirects=False);t=r.cookies.get('access_token');assert t
    r=c.post('/api/generate-home',json={'budget':50000,'rooms':['Living Room'],'items':['Sofa'],'style':'Modern','city':'Chennai'},cookies={'access_token':t});assert r.status_code==200;assert r.json()['planner']=='home'
def test_protected():assert c.get('/api/history').status_code==401
