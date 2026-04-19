from app.utils.mysql_db import SessionLocal
from sqlalchemy.orm.exc import StaleDataError
from app.models.product import Product
import pytest
from app.models.user import User
from app.utils.mysql_db import SessionLocal

def test_optimistic_locking(setup_product):
    
    prod_id = setup_product.id

    session_a = SessionLocal()
    session_b = SessionLocal()

    prod_a = session_a.get(Product, prod_id)
    prod_b = session_b.get(Product, prod_id)

    print(f"[Initial] Session A version: {prod_a.version}, Session B version: {prod_b.version}")
    
    prod_a.name = "Price updated by A"
    session_a.commit()
    print(f"[Step 1] Session A commited. DB version is now 2. ")

    prod_b.name = "Price updated by B"
    print(f"[Step 2] Session B attemptes to commit with version 1..." )

    with pytest.raises(StaleDataError) as excinfo:
        session_b.commit()
    
    print(f"[Success] caught expected error: {excinfo.type.__name__}")

    session_a.close()
    session_b.close()

    