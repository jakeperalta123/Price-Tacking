import requests
from urllib.parse import quote_plus, urlencode
from bs4 import BeautifulSoup
from app.core.celery_app import celery_app
from app.models import Product, Price
from app.core.config import settings
from app.db import SessionLocal


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
        print(f"DEBUG: Status Code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')

        price_element = soup.select_one('div[data-automation-id="product-price"]')

        if price_element:
            raw_price = price_element.get_text().replace('$', '').replace(',', '')
            db = SessionLocal()
            new_price = Price(product_id=product_id, price=float(raw_price), source=settings.SOURCE_NAME_WALMART)
            db.add(new_price)
            db.commit()
            db.close()
            return f"成功爬取{product_name}: {raw_price}"
        return f"找不到{product_name}的價格"
    
    except Exception as e:
        return f"爬取失敗: {str(e)}"

@celery_app.task(name="daily_noon_check")
def daily_noon_check():
    db = SessionLocal()
    monitored_products = db.query(Product).filter(Product.is_monitored == True).all()

    for product in monitored_products:
        scrape_walmart_by_name.delay(product.id, product.name)
    
    db.close()
    return f"已發送{len(monitored_products)}個爬蟲任務"