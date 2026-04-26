import pytest
from app.services.scraper import extract_price
from app.crud.price_crud import create_price_entry
from app.models.product import Product
from app.models.user import User
from app.models.price import Price
from decimal import Decimal
from app.tasks.scraper_tasks import scrape_walmart_by_name
from unittest.mock import patch

@patch("app.tasks.scraper_tasks.requests.get")
def test_full_task_integration(mock_get, db_session):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '<div data-automation-id="product-price">$888.88</div>'

    test_user = User(username="elon", email="2@gmail.com", password_hash="hash")
    db_session.add(test_user)
    db_session.flush()

    test_product = Product(name="test product 1", user_id=test_user.id, is_monitored=True)
    db_session.add(test_product)
    db_session.commit()

    result = scrape_walmart_by_name(test_product.id, test_product.name)
    assert "成功爬取" in result
    assert "888.88" in result
    assert mock_get.called

def test_scraper_to_db(db_session):
    fake_html = '<div data-automation-id="product-price">$888.88</div>'
    price = extract_price(fake_html)
    assert price == 888.88
    test_user = User(username="Jake", email="1@gmail.com", password_hash="fake hash")
    db_session.add(test_user)
    db_session.flush()
    test_product = Product(name="Test product",user_id=test_user.id)
    db_session.add(test_product)
    db_session.commit()

    result = create_price_entry(db_session, product_id=test_product.id, price=price, source="test")
    saved_entry = db_session.query(Price).filter(Price.product_id==test_product.id).first()
    assert saved_entry is not None
    assert saved_entry.price == Decimal("888.88")

    print("test successful, db is clean")
    

def test_price_idempotency_logic(db_session):
    import uuid
    
    unique_id = uuid.uuid4().hex[:6]
    test_user = User(
        username=f"tester{unique_id}",
        email=f"{unique_id}@test.com",
        password_hash="hash"
                     )
    db_session.add(test_user)
    db_session.flush()

    test_product = Product(
        user_id=test_user.id,
        name="Idempotency Item"
        )
    
    db_session.add(test_product)
    db_session.commit()

    price_val = Decimal('100.00')
    source_val = "walmart"

    create_price_entry(db_session, test_product.id, price_val, source_val)
    create_price_entry(db_session, test_product.id, price_val, source_val)

    count = db_session.query(Price).filter(Price.product_id == test_product.id).count()
    assert count == 1, f"Idempotency not working!, Expected count to be 1, but db stored {count} times"
    print(f"Idempotency works: The second attempt within is intercepted")

