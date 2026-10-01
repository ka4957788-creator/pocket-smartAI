from pydantic import BaseModel,Field
class HomeRequest(BaseModel):
    budget:float=Field(gt=0); rooms:list[str]=Field(min_length=1); items:list[str]=Field(min_length=1); style:str='Modern'; city:str='Chennai'
class PartyRequest(BaseModel):
    budget:float=Field(gt=0); guests:int=Field(gt=0); event_type:str; venue:str='Not decided'; city:str='Chennai'; preferences:str=''
class RecItem(BaseModel):
    category:str; name:str; platform:str; estimated_price:float; quantity:int=1; reason:str; search_url:str
class Breakdown(BaseModel): category:str; amount:float; percentage:float
class Recommendation(BaseModel):
    planner:str; budget:float; estimated_total:float; remaining_budget:float; summary:str; budget_breakdown:list[Breakdown]; recommendations:list[RecItem]; disclaimer:str
