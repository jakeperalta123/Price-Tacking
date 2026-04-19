import pytest
from httpx import AsyncClient
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.base import Base
from app.models.user import User
from app.models.product import Product
from app.utils.security import get_current_user
from app.db import getSession
import fakeredis.aioredis as fakeredis
from app.api.deps import get_redis
from app.utils.mysql_db import SessionLocal as MySQLSessionLocal

TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def test_app():
    return app

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(autouse=True)
def override_get_session(db_session):
    def _override():
        yield db_session

    app.dependency_overrides[getSession] = _override
    yield
    app.dependency_overrides.pop(getSession, None)

@pytest.fixture
def mysql_db():
    session = MySQLSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def setup_product(mysql_db):
    test_user = mysql_db.query(User).filter(User.id == 1).first()
    if not test_user:
        test_user = User(
            id=1, 
            username="jake_test",     
            email="test@example.com", 
            password_hash="fake_hash_for_test" 
        )
        mysql_db.add(test_user)
        mysql_db.commit()

    test_prod = Product(name="MacBook M3", user_id=1)
    mysql_db.add(test_prod)
    mysql_db.commit()

    yield test_prod
    mysql_db.rollback()

    latest_prod = mysql_db.get(Product, test_prod.id)
    if latest_prod:
        mysql_db.delete(latest_prod)
        mysql_db.commit()

@pytest.fixture
async def fake_redis():
    fake_engine = fakeredis.FakeRedis(decode_responses=True)
    from app.core.redis import RedisCache
    wrapper = RedisCache()
    wrapper.redis = fake_engine
    yield wrapper
    await fake_engine.flushdb()
    await fake_engine.aclose()

@pytest.fixture(autouse=True)
def override_redis_dependency(fake_redis):
    async def _override():
        return fake_redis
    app.dependency_overrides[get_redis] = _override
    yield 
    app.dependency_overrides.pop(get_redis, None)

@pytest.fixture
def test_user():
    return User(id=1, email="test@example.com", username="Test User")

@pytest.fixture()
def override_get_current_user(test_user):
    
    async def _override():
        return test_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture()
async def async_client(override_get_current_user, override_get_session):
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client