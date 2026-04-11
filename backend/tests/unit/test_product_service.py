import pytest
from unittest.mock import MagicMock, AsyncMock
from app.services.product_service import check_and_trigger_monitoring

class TestCheckAndTriggerMonitoring:

    @pytest.mark.asyncio
    async def test_first_input_no_trigger(self, mock_redis):

        mock_redis.incr.return_value = 1
        mock_session = MagicMock()

        result = await check_and_trigger_monitoring(1, 'Product A', mock_session, redis=mock_redis)
        
        assert result == (False, 1)
        mock_redis.incr.assert_called_once()
        mock_session.query.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_second_input_no_trigger(self, mock_redis):

        mock_redis.incr.return_value = 2
        mock_session = MagicMock()

        result = await check_and_trigger_monitoring(1, 'Product A', mock_session, redis=mock_redis)
        
        assert result == (False, 2)
        mock_redis.incr.assert_called_once()
        mock_session.query.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_third_input_triggers_monitoring(self, mock_redis, mock_celery):        
        
        mock_redis.incr.return_value = 3
        mock_product = MagicMock()
        mock_product.id = 123
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_product
        
        result = await check_and_trigger_monitoring(1, 'Product A', mock_session, redis=mock_redis)
        
        assert result == (True, 3)

        assert mock_product.is_monitored == True
        mock_session.commit.assert_called_once()
        mock_celery.delay.assert_called_once_with(123, 'Product A')
        mock_redis.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_triggered_but_product_not_found(self, mock_redis):
        mock_redis.incr.return_value = 3
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        result = await check_and_trigger_monitoring(1, 'Prduct A', mock_session, redis=mock_redis)
        
        assert result == (False, 3)

        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_redis_key_format(self, mock_redis):
        import hashlib

        mock_session = MagicMock()
        product_name = 'test product'
        user_id = 2047
        expected_hash = hashlib.md5(product_name.encode()).hexdigest()
        expected_key = f"counter:{user_id}:{expected_hash}"
        
        await check_and_trigger_monitoring(user_id, product_name, mock_session, redis=mock_redis)
        mock_redis.incr.assert_called_once_with(expected_key)