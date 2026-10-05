from typing import Literal
from pydantic import BaseModel, Field
class ItemRequest(BaseModel):
    name: str=Field(min_length=1,max_length=100); quantity:int=Field(1,ge=1,le=50)
class HomeRequest(BaseModel):
    room_type: Literal["Living Room","Kitchen","Bedroom","Dining Room","Home Office","Other"]="Living Room"
    budget:float=Field(gt=0,le=10_000_000); style:str=Field("modern",min_length=1,max_length=80)
    items:list[ItemRequest]=Field(min_length=1,max_length=30); notes:str=Field("",max_length=1000)
class PartyRequest(BaseModel):
    budget:float=Field(gt=0,le=10_000_000); guest_count:int=Field(gt=0,le=5000)
    event_type:str=Field(min_length=1,max_length=80); venue:str=Field("home",max_length=120)
    food_preference:str=Field("mixed",max_length=80); theme:str=Field("simple",max_length=100); notes:str=Field("",max_length=1000)
class JewelryRequest(BaseModel):
    budget:float=Field(gt=0,le=10_000_000); occasion:str=Field(min_length=1,max_length=100)
    style:str=Field("elegant",max_length=100); metal_preference:str=Field("any",max_length=50); notes:str=Field("",max_length=1000)
class ProductRecommendation(BaseModel):
    name:str; category:str; platform:str; estimated_price:float=Field(ge=0); quantity:int=Field(1,ge=1); reason:str; url:str
class BudgetAllocation(BaseModel):
    category:str; amount:float=Field(ge=0); percentage:float=Field(ge=0,le=100)
class RecommendationResponse(BaseModel):
    planner:str; title:str; summary:str; allocations:list[BudgetAllocation]; recommendations:list[ProductRecommendation]
    total_estimated:float=Field(ge=0); remaining_budget:float; tips:list[str]=[]; ai_used:bool=False; image_insight:str|None=None
