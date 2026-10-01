import json
from .database import get_db
def save_recommendation(uid,planner,inp,res):
    with get_db() as c:c.execute('INSERT INTO recommendations(user_id,planner_type,input_json,result_json) VALUES(?,?,?,?)',(uid,planner,json.dumps(inp),json.dumps(res)))
