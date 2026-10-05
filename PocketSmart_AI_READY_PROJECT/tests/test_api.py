import os
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db";os.environ["SECRET_KEY"]="test-secret"
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base,engine
Base.metadata.drop_all(bind=engine);Base.metadata.create_all(bind=engine)
c=TestClient(app)
def test_auth_and_home_fallback():
    assert c.post('/register',json={"full_name":"Test User","email":"test@example.com","password":"password123"}).status_code==200
    assert c.get('/session-info').status_code==200
    r=c.post('/generate-home',json={"room_type":"Living Room","budget":80000,"style":"modern","items":[{"name":"Sofa","quantity":1},{"name":"Lamp","quantity":2}],"notes":""})
    assert r.status_code==200; assert r.json()["remaining_budget"]>=0
    assert len(c.get('/history').json())>=1
