from datetime import datetime,timedelta,timezone
import jwt
from passlib.context import CryptContext
from fastapi import Request,HTTPException
from .config import get_settings
from .database import get_db
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto')
def hash_password(x): return pwd.hash(x)
def verify_password(x,h): return pwd.verify(x,h)
def token(uid):
    exp=datetime.now(timezone.utc)+timedelta(minutes=get_settings().access_token_expire_minutes)
    return jwt.encode({'sub':str(uid),'exp':exp},get_settings().secret_key,algorithm='HS256')
def current_user(request:Request):
    t=request.cookies.get('access_token') or request.headers.get('Authorization','').removeprefix('Bearer ').strip()
    if not t: raise HTTPException(401,'Authentication required')
    try: uid=int(jwt.decode(t,get_settings().secret_key,algorithms=['HS256'])['sub'])
    except Exception: raise HTTPException(401,'Invalid or expired token')
    with get_db() as c:r=c.execute('SELECT id,name,email FROM users WHERE id=?',(uid,)).fetchone()
    if not r: raise HTTPException(401,'User not found')
    return dict(r)
def optional_user(request):
    try:return current_user(request)
    except HTTPException:return None
