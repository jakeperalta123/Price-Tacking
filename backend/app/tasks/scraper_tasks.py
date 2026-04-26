import requests
from urllib.parse import quote_plus, urlencode
from bs4 import BeautifulSoup
from app.core.celery_app import celery_app
from app.models import Product, Price
from app.core.config import settings
from app.db import SessionLocal
from app.crud.price_crud import create_price_entry
from app.services.scraper import extract_price

@celery_app.task(name="scrape_walmart_by_search")
def scrape_walmart_by_name(product_id: int, product_name: str):
    target_url = f"{settings.WALMART_SEARCH_BASE_URL}?q={quote_plus(product_name)}"
    params = {
        'api_key': settings.SCRAPER_API_KEY, 
        'url': target_url,
        'render': 'true'
    }
    proxy_url = "https://api.scraperapi.com/?" + urlencode(params)

    try: 
        response = requests.get(proxy_url, timeout=settings.SCRAPE_TIMEOUT)
        with open("debug_walmart.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        if response.status_code != 200:
            return f"scraping failed: HTTP{response.status_code}"
        
        price = extract_price(response.text)

        if price is not None:
            with SessionLocal() as db:
                create_price_entry(
                    db=db, 
                    product_id=product_id,
                    price=price,
                    source=settings.SOURCE_NAME_WALMART
                )
            return f"成功爬取 {product_name}: {price}"
        
        return f"找不到 {product_name} 的價格欄位"
    except Exception as e:
        return f"task failed: {str(e)}"


@celery_app.task(name="daily_noon_check")
def daily_noon_check():
    db = SessionLocal()
    monitored_products = db.query(Product).filter(Product.is_monitored == True).all()

    for product in monitored_products:
        scrape_walmart_by_name.delay(product.id, product.name)
    
    db.close()
    return f"已發送{len(monitored_products)}個爬蟲任務"