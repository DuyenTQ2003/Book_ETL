from fastapi import FastAPI
from routers.book_api import router as book_router
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from config.log import logger

app = FastAPI()

# Register routes
app.include_router(book_router, tags=["Books"])

@app.on_event("startup")
async def run_etl():
    logger.info("Running ETL process")
    data = extract_data()
    if data:
        transformed_data = transform_data(data)
        load_data(transformed_data)
        logger.info("ETL process completed")
