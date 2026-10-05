from app.services.allocator import allocate_home,allocate_party
def test_home_allocation_balances_to_budget():
    p=allocate_home(80000,[{"name":"Sofa","quantity":1},{"name":"Lamp","quantity":2}]);assert p["allocated"]==80000;assert p["remaining"]==0
def test_party_allocation_balances_to_budget():
    p=allocate_party(50000,30);assert p["allocated"]==50000;assert p["remaining"]==0


def test_home_fallback_never_exceeds_tiny_budget():
    from app.schemas import HomeRequest
    from app.services.recommendation import fallback_home
    result = fallback_home(HomeRequest(room_type="Living Room", budget=1000, style="modern", items=[{"name":"Lamp","quantity":1}], notes=""))
    assert result.total_estimated <= 1000
    assert result.remaining_budget >= 0
