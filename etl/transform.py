from config.log import logger

def transform_data(data):
    logger.info("Starting data transformation")
    for item in data:
        item["price"] = item["price"].replace("Â", "").strip()
        item["title"] = item["title"].capitalize()
    logger.info("Data transformation complete")
    return data
