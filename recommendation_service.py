from .gemini_service import gemini
from .platform_links import platform_url
from ..schemas import Recommendation
RULES='''You are PocketSmart AI. Return ONLY valid JSON. Make budget-aware recommendations for India. Do not claim live inventory. Estimated prices are planning estimates. Keep estimated total within budget. Platforms allowed: Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO.'''
def normalize(d,planner,budget):
    d.setdefault('planner',planner);d.setdefault('budget',budget);d.setdefault('summary','Budget-aware plan generated.');d.setdefault('budget_breakdown',[]);d.setdefault('recommendations',[])
    for x in d['recommendations']: x['search_url']=platform_url(x.get('platform','Amazon'),x.get('name','product'))
    total=sum(float(x.get('estimated_price',0))*int(x.get('quantity',1)) for x in d['recommendations']);d['estimated_total']=round(total,2);d['remaining_budget']=round(budget-total,2);d['disclaimer']='Prices are estimates. Check the linked platform for current price, availability, taxes and delivery.'
    return Recommendation.model_validate(d).model_dump()
def fallback(planner,budget,data):
    if planner=='home': items=[('Furniture','Compact dining table','IKEA',.18,'Useful furniture while controlling space and cost.'),('Lighting','LED ceiling light set','Amazon',.10,'Improves lighting without using a large share of the budget.'),('Decor','Wall art set','Amazon',.08,'Adds visual character at a moderate cost.')]; bd=[('Furniture',45),('Lighting',20),('Decor',20),('Contingency',15)]
    elif planner=='party': items=[('Food',f"{data.get('guests',20)}-guest catering options",'Zomato',.45,'Keeps food as the main event expense.'),('Venue',data.get('venue','event venue'),'OYO',.22,'Useful starting point for venue/accommodation searches.'),('Decoration','Event decoration kit','Amazon',.12,'Creates a theme without overspending.')]; bd=[('Food',50),('Venue',25),('Decoration',15),('Contingency',10)]
    else: items=[('Main piece',f"{data.get('style','elegant')} necklace set",'Amazon',.45,'A versatile statement piece for the occasion.'),('Matching piece','Matching earrings','Flipkart',.20,'Complements the main jewelry choice.')]; bd=[('Main piece',60),('Matching piece',25),('Contingency',15)]
    raw={'summary':'A practical starter plan based on your budget and preferences.','budget_breakdown':[{'category':a,'amount':round(budget*p/100,2),'percentage':p} for a,p in bd],'recommendations':[{'category':a,'name':n,'platform':p,'estimated_price':round(budget*share,2),'quantity':1,'reason':r} for a,n,p,share,r in items]};return normalize(raw,planner,budget)
def generate(planner,budget,data,image=None,mime=None):
    prompt=RULES+f'\nPlanner: {planner}\nUser data: {data}\nReturn keys planner,budget,estimated_total,remaining_budget,summary,budget_breakdown,recommendations,disclaimer.'
    try:
        if gemini.client:return normalize(gemini.generate(prompt,image,mime),planner,budget)
    except Exception: pass
    return fallback(planner,budget,data)
