import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    WALMART_SEARCH_BASE_URL: str = "https://www.walmart.com/search"
    SCRAPE_TIMEOUT: int = 60
    SCRAPER_API_KEY: str
    SOURCE_NAME_WALMART: str = "walmart_search"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()