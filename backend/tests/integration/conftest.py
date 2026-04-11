import pytest
from httpx import AsyncClient
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.base import Base
from app.models.user import User
from app.utils.security import get_current_user
from app.db import getSession
import fakeredis.aioredis as fakeredis
from app.api.deps import get_redis

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