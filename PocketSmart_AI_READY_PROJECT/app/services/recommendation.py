from app.schemas import *
from app.services.allocator import allocate_home,allocate_party
from app.services.catalog import search_catalog
def select(candidates,budget,limit=6):
    out=[]; total=0
    for x in sorted(candidates,key=lambda z:z["estimated_price"]):
        price=float(x["estimated_price"])
        if total + price > budget * .92:
            continue
        out.append(ProductRecommendation(name=x["name"],category=x["category"],platform=x["platform"],estimated_price=price,reason="Fits the budget profile and matches the selected planner category.",url=x["url"]))
        total += price
        if len(out)>=limit:break
    return out
def fallback_home(r):
    a=allocate_home(r.budget,[x.model_dump() for x in r.items]); p=select(search_catalog("home",r.budget,[x.name for x in r.items]),r.budget); t=round(sum(x.estimated_price for x in p),2)
    return RecommendationResponse(planner="home",title=f"{r.style.title()} {r.room_type} Plan",summary=f"A practical {r.style} setup for your {r.room_type.lower()}, prioritizing the requested items.",allocations=[BudgetAllocation(**x) for x in a["allocations"]],recommendations=p,total_estimated=t,remaining_budget=round(r.budget-t,2),tips=["Prioritize high-use furniture before decorative pieces.","Compare delivery charges and dimensions before purchasing.","Verify retailer prices before buying."],ai_used=False)
def fallback_party(r):
    a=allocate_party(r.budget,r.guest_count); c=search_catalog("party",r.budget); rows=[]
    for x in c:
        x=dict(x)
        if x["category"]=="Catering":x["estimated_price"]*=r.guest_count
        if x["estimated_price"]<=r.budget*.75:rows.append(x)
    p=select(rows,r.budget,5);t=round(sum(x.estimated_price for x in p),2)
    return RecommendationResponse(planner="party",title=f"{r.event_type.title()} Party Plan",summary=f"A {r.guest_count}-guest {r.event_type.lower()} plan using your {r.theme} theme and {r.food_preference} food preference.",allocations=[BudgetAllocation(**x) for x in a["allocations"]],recommendations=p,total_estimated=t,remaining_budget=round(r.budget-t,2),tips=["Confirm per-person catering charges before booking.","Keep contingency for taxes, transport and last-minute purchases.","Ask venues what is included."],ai_used=False)
def fallback_jewelry(r,insight=None):
    p=select(search_catalog("jewelry",r.budget),r.budget,5);t=round(sum(x.estimated_price for x in p),2)
    return RecommendationResponse(planner="jewelry",title=f"{r.occasion.title()} Jewelry Edit",summary=f"Style-matched jewelry ideas for a {r.occasion.lower()} occasion with a {r.style} preference.",allocations=[BudgetAllocation(category="Primary piece",amount=round(r.budget*.65,2),percentage=65),BudgetAllocation(category="Supporting piece",amount=round(r.budget*.25,2),percentage=25),BudgetAllocation(category="Buffer",amount=round(r.budget*.1,2),percentage=10)],recommendations=p,total_estimated=t,remaining_budget=round(r.budget-t,2),tips=["Match jewelry scale to the outfit neckline and visual balance.","Prioritize comfort and secure closures for regular wear.","Verify metal purity, seller policies and returns."],ai_used=False,image_insight=insight)
