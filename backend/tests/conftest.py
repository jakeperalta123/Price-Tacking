import pytest
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.fixture(autouse=True)
def mock_app_config():
    # Mock settings before any app imports
    mock_settings = MagicMock()
    mock_settings.WALMART_SEARCH_BASE_URL = "https://www.walmart.com/search"
    mock_settings.SCRAPE_TIMEOUT = 60
    mock_settings.SCRAPER_API_KEY = "test_api_key"
    mock_settings.SOURCE_NAME_WALMART = "walmart_search"   
    
    with patch('app.core.config.settings', mock_settings):
        yield