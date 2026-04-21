import pytest
from unittest.mock import patch, MagicMock, AsyncMock



mock_redis_obj = AsyncMock()
redis_patcher = patch('app.core.redis.redis_client', mock_redis_obj)
redis_patcher.start()

mock_celery_obj = MagicMock()
celery_patcher = patch('app.services.product_service.scrape_walmart_by_name', mock_celery_obj)
celery_patcher.start()


@pytest.fixture(autouse=True)
def mock_redis():
        mock_redis_obj.reset_mock()
        mock_redis_obj.incr.return_value = 1  # Default return value
        yield mock_redis_obj

@pytest.fixture(autouse=True)
def mock_celery():
        mock_celery_obj.reset_mock()
        yield mock_celery_obj