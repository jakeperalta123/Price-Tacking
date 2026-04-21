from app.db import SessionLocal
from sqlalchemy.orm.exc import StaleDataError
from app.models.product import Product
import pytest
from app.models.user import User
from sqlalchemy import func

def test_optimistic_locking():
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

        max_id = session.query(func.max(Product.id)).scalar()
        if max_id is None:
            max_id = 0

        test_prod = Product(name=f"MacBook M3 {max_id + 1}", user_id=1)
        session.add(test_prod)
        session.commit()
        prod_id = test_prod.id
        
    finally:
        session.close()

    session_a = SessionLocal()
    session_b = SessionLocal()

    try:
        prod_a = session_a.get(Product, prod_id)
        prod_b = session_b.get(Product, prod_id)

        assert prod_a is not None, f"Product with id {prod_id} not found"
        assert prod_b is not None, f"Product with id {prod_id} not found"

        print(f"[Initial] Session A version: {prod_a.version}, Session B version: {prod_b.version}")
        
        prod_a.name = "Price updated by A"
        session_a.commit()
        print(f"[Step 1] Session A commited. DB version is now {prod_a.version}. ")

        prod_b.name = "Price updated by B"
        print(f"[Step 2] Session B attemptes to commit with version {prod_b.version}..." )

        with pytest.raises(StaleDataError) as excinfo:
            session_b.commit()
        
        print(f"[Success] caught expected error: {excinfo.type.__name__}")

    finally:
        session_a.close()
        session_b.close()

    