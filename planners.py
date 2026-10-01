from fastapi import APIRouter,Depends,File,Form,UploadFile,HTTPException
from ..auth import current_user
from ..schemas import HomeRequest,PartyRequest
from ..services.recommendation_service import generate
from ..dependencies import save_recommendation
r=APIRouter()
@r.post('/generate-home')
def home(x:HomeRequest,u=Depends(current_user)):
    out=generate('home',x.budget,x.model_dump());save_recommendation(u['id'],'home',x.model_dump(),out);return out
@r.post('/generate-party')
def party(x:PartyRequest,u=Depends(current_user)):
    out=generate('party',x.budget,x.model_dump());save_recommendation(u['id'],'party',x.model_dump(),out);return out
@r.post('/generate-jewelry')
async def jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form('Elegant'),outfit_description:str=Form(''),outfit_image:UploadFile|None=File(None),u=Depends(current_user)):
    image=None;mime=None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {'image/jpeg','image/png','image/webp'}:raise HTTPException(400,'Only JPG, PNG or WEBP images are supported')
        image=await outfit_image.read();mime=outfit_image.content_type
        if len(image)>5*1024*1024:raise HTTPException(413,'Image must be under 5 MB')
    data={'budget':budget,'occasion':occasion,'style':style,'outfit_description':outfit_description};out=generate('jewelry',budget,data,image,mime);save_recommendation(u['id'],'jewelry',data,out);return out
