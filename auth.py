from fastapi import APIRouter,Form
from fastapi.responses import RedirectResponse,JSONResponse
from ..database import get_db
from ..auth import hash_password,verify_password,token
r=APIRouter()
@r.post('/register')
def register(name:str=Form(...),email:str=Form(...),password:str=Form(...)):
    with get_db() as c:
        if c.execute('SELECT id FROM users WHERE email=?',(email.lower(),)).fetchone():return JSONResponse({'error':'Email already registered'},400)
        uid=c.execute('INSERT INTO users(name,email,password_hash) VALUES(?,?,?)',(name,email.lower(),hash_password(password))).lastrowid
    x=RedirectResponse('/dashboard',303);x.set_cookie('access_token',token(uid),httponly=True,samesite='lax');return x
@r.post('/login')
def login(email:str=Form(...),password:str=Form(...)):
    with get_db() as c:u=c.execute('SELECT id,password_hash FROM users WHERE email=?',(email.lower(),)).fetchone()
    if not u or not verify_password(password,u['password_hash']):return JSONResponse({'error':'Invalid email or password'},401)
    x=RedirectResponse('/dashboard',303);x.set_cookie('access_token',token(u['id']),httponly=True,samesite='lax');return x
@r.post('/logout')
def logout():
    x=RedirectResponse('/',303);x.delete_cookie('access_token');return x
@r.post('/token')
def api_token(email:str=Form(...),password:str=Form(...)):
    with get_db() as c:u=c.execute('SELECT id,password_hash FROM users WHERE email=?',(email.lower(),)).fetchone()
    if not u or not verify_password(password,u['password_hash']):return JSONResponse({'error':'Invalid credentials'},401)
    return {'access_token':token(u['id']),'token_type':'bearer'}
