def _allocate(budget,weights):
    total=sum(max(w,0) for _,w in weights) or 1; out=[]; used=0
    for i,(name,w) in enumerate(weights):
        amount=round(budget-used,2) if i==len(weights)-1 else round(budget*max(w,0)/total,2)
        used+=amount; out.append({"category":name,"amount":amount,"percentage":round(amount/budget*100,2)})
    return {"allocated":round(sum(x["amount"] for x in out),2),"remaining":round(budget-sum(x["amount"] for x in out),2),"allocations":out}
def allocate_home(budget,items):
    weights=[]
    for x in items:
        n=x.get("name","Item"); q=max(int(x.get("quantity",1)),1); m=2 if any(k in n.lower() for k in ("sofa","bed","table","wardrobe","cabinet")) else 1
        weights.append((n,q*m))
    return _allocate(float(budget),weights)
def allocate_party(budget,guest_count):
    g=max(1,min(guest_count/50,2)); return _allocate(float(budget),[("Catering",50*g),("Venue",20),("Decoration",15),("Entertainment",10),("Contingency",5)])
