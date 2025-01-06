"""Module providing a function printing python version."""
import requests
from parsel import Selector
from config.log import logger

BOOKS_URL = "https://books.toscrape.com/"

def extract_data() -> list:
    """
    Extract data from the Books to Scrape website.

    This function sends a GET request to the BOOKS_URL, parses the response using XPath,
    and extracts information about books, including their title, price, and availability status.

    Returns:
        list: A list of dictionaries, where each dictionary contains the following keys:
            - title (str): The title of the book.
            - price (str): The price of the book as displayed on the website.
            - availability (str): The availability status of the book (e.g., "In stock").

    Logs:
        - Info: When the extraction starts and ends, including the number of books extracted.
        - Error: If the request fails, logs the failure with the status code.

    Example Output:
    [
        {
            "title": "A Light in the Attic",
            "price": "£51.77",
            "availability": "In stock (22 available)"
        },
        {
            "title": "Tipping the Velvet",
            "price": "£53.74",
            "availability": "In stock (20 available)"
        }
    ]
    """
    logger.info("Starting data extraction")
    response = requests.get(BOOKS_URL,timeout=10)
    if response.status_code != 200:
        logger.error(f"Failed to fetch data from: %s , status code: {response.status_code}",BOOKS_URL)
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
    logger.info("Extracted %d books",len(books))
    return books
