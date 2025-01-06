from pydantic import BaseModel

class Book(BaseModel):
    title: str
    price: str
    availability: str

class BookInDB(Book):
    id: str