import json
from fastapi import APIRouter,Depends
from ..auth import current_user
from ..database import get_db
r=APIRouter()
@r.get('/history')
def history(u=Depends(current_user)):
    with get_db() as c: rows=c.execute('SELECT id,planner_type,input_json,result_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC',(u['id'],)).fetchall()
    return [{'id':x['id'],'planner_type':x['planner_type'],'input':json.loads(x['input_json']),'result':json.loads(x['result_json']),'created_at':x['created_at']} for x in rows]
