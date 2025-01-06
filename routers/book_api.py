from fastapi import APIRouter, HTTPException
from models.schema import Book, BookInDB
from config.database import db
from bson import ObjectId

router = APIRouter()

@router.get("/books", response_model=list[BookInDB])
async def get_books():
    books = list(db["books"].find())
    return [{"id": str(book["_id"]), **book} for book in books]

@router.get("/books/{book_id}", response_model=BookInDB)
async def get_book(book_id: str):
    book = db["books"].find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": str(book["_id"]), **book}

@router.post("/books", response_model=BookInDB)
async def create_book(book: Book):
    result = db["books"].insert_one(book.dict())
    return {"id": str(result.inserted_id), **book.dict()}

@router.put("/books/{book_id}", response_model=BookInDB)
async def update_book(book_id: str, book: Book):
    result = db["books"].update_one({"_id": ObjectId(book_id)}, {"$set": book.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, **book.dict()}

@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    result = db["books"].delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
