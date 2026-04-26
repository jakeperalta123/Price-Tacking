from bs4 import BeautifulSoup
import re

def extract_price(html_text: str) -> float:
    if not html_text:
        return None
    
    soup = BeautifulSoup(html_text, 'html.parser')
    price_element = soup.select_one('div[data-automation-id="product-price"]')

    if not price_element:
        return None
    
    raw_price = price_element.get_text().replace('$', '').replace(',', '')

    match = re.search(r"[-+]?\d*\.\d+|\d+", raw_price)

    return float(match.group()) if match else None