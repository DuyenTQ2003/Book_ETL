import requests
from parsel import Selector
from config.log import logger

BOOKS_URL = "https://books.toscrape.com/"

def extract_data():
    logger.info("Starting data extraction")
    response = requests.get(BOOKS_URL)
    if response.status_code != 200:
        logger.error(f"Failed to fetch data from {BOOKS_URL}, status code: {response.status_code}")
        return []

    selector = Selector(response.text)
    books = []
    for book in selector.xpath("//article[@class='product_pod']"):
        title = book.xpath(".//h3/a/@title").get()
        price = book.xpath(".//p[@class='price_color']/text()").get()
        availability = book.xpath(".//p[contains(@class, 'availability')]/text()").getall()
        availability = "".join(availability).strip()
        books.append({
            "title": title,
            "price": price,
            "availability": availability
        })
    logger.info(f"Extracted {len(books)} books")
    return books
