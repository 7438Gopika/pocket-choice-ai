from app.config import get_settings
from app.schemas import *
from app.services.recommendation import fallback_home,fallback_party,fallback_jewelry

def _call(prompt,image=None,mime=None):
    s=get_settings()
    if not s.gemini_api_key: raise RuntimeError("GEMINI_API_KEY is not configured")
    from google import genai
    from google.genai import types
    c=genai.Client(api_key=s.gemini_api_key); parts=[prompt]
    if image: parts.append(types.Part.from_bytes(data=image,mime_type=mime or "image/jpeg"))
    res=c.models.generate_content(model=s.gemini_model,contents=parts,config=types.GenerateContentConfig(temperature=.35,response_mime_type="application/json",response_schema=RecommendationResponse))
    return RecommendationResponse.model_validate_json(res.text)
def catalog_text(c): return str([{k:x[k] for k in ("name","category","platform","estimated_price","url")} for x in c])
def home(r,c):
    p=f"""You are PocketSmart AI. Create a practical home recommendation. Use ONLY this catalog: {catalog_text(c)}. User: {r.model_dump_json()}. Respect the budget. Never invent products, prices, platforms or URLs. Keep total_estimated <= budget. Return JSON matching the supplied schema. planner must be home and ai_used true."""
    return _call(p)
def party(r,c):
    p=f"""You are PocketSmart AI. Create a party budget plan. Use ONLY this catalog: {catalog_text(c)}. User: {r.model_dump_json()}. Respect budget and guest count. Never invent products, prices, platforms or URLs. Keep total_estimated <= budget. Return JSON matching the supplied schema. planner must be party and ai_used true."""
    return _call(p)
def jewelry(r,c,image=None,mime=None):
    p=f"""You are PocketSmart AI. Recommend jewelry for this user: {r.model_dump_json()}. Use ONLY this catalog: {catalog_text(c)}. Respect budget. If an outfit image is attached, infer only visible colors, neckline and style; do not identify the person. Never invent products, prices, platforms or URLs. Keep total_estimated <= budget. Return JSON matching the supplied schema, set planner to jewelry and ai_used true, and provide image_insight when an image is present."""
    return _call(p,image,mime)
def safe_home(r,c):
    try:return home(r,c)
    except Exception:return fallback_home(r)
def safe_party(r,c):
    try:return party(r,c)
    except Exception:return fallback_party(r)
def safe_jewelry(r,c,image=None,mime=None):
    try:return jewelry(r,c,image,mime)
    except Exception:return fallback_jewelry(r,"The image was received, but AI image analysis was unavailable; recommendations use your text preferences." if image else None)
