import pytest
from httpx import AsyncClient
from app.models.user import User
from app.db import SessionLocal

@pytest.mark.asyncio
async def test_trigger_monitoring_sequence(async_client: AsyncClient, fake_redis):
    # Ensure test user exists in DB
    session = SessionLocal()
    try:
        test_user = session.get(User, 1)
        if not test_user:
            test_user = User(
                id=1, 
                username="jake_test",     
                email="test@example.com", 
                password_hash="fake_hash_for_test" 
            )
            session.add(test_user)
            session.commit()
    finally:
        session.close()

    product_payload = {
        "name": "Switch OLED", 
        "unit": "each", 
        "price": 350.0, 
        "category": "gaming"
    }

    response1 = await async_client.post("/products/price", json=product_payload)
    print(f"/nDebug Response: {response1.json()}")
    assert response1.status_code == 200
    assert "目前次數:1" in response1.json()["message"]

    response2 = await async_client.post("/products/price", json=product_payload)
    assert "目前次數:2" in response2.json()["message"]

    response3 = await async_client.post("/products/price", json=product_payload)
    assert "已開啟每日監控" in response3.json()["message"]