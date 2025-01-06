"""Module providing a function printing python version."""
from fastapi import APIRouter,HTTPException
from bson import ObjectId
from models.schema import Book,BookInDB
from config.database import db

router = APIRouter()

@router.get("/books", response_model=list[BookInDB])
async def get_books():
    """
    Retrieve all books from the database.

    Returns:
        list[BookInDB]: A list of all books stored in the database, including their IDs.

    Example Response:
    [
        {
            "id": "string",
            "title": "string",
            "author": "string",
            "description": "string"
        }
    ]
    """
    books = list(db["books"].find())
    return [{"id": str(book["_id"]), **book} for book in books]

@router.get("/books/{book_id}", response_model=BookInDB)
async def get_book(book_id: str):
    """
    Retrieve a specific book by its ID.

    Args:
        book_id (str): The ID of the book to retrieve.

    Returns:
        BookInDB: The details of the requested book.

    Raises:
        HTTPException: If the book with the given ID does not exist.

    Example Response:
    {
        "id": "string",
        "title": "string",
        "author": "string",
        "description": "string"
    }
    """
    book = db["books"].find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": str(book["_id"]), **book}

@router.post("/books", response_model=BookInDB)
async def create_book(book: Book):
    """
    Create a new book entry in the database.

    Args:
        book (Book): The book details to add to the database.

    Returns:
        BookInDB: The details of the newly created book, including its ID.

    Example Response:
    {
        "id": "string",
        "title": "string",
        "author": "string",
        "description": "string"
    }
    """
    result = db["books"].insert_one(book.dict())
    return {"id": str(result.inserted_id), **book.dict()}

@router.put("/books/{book_id}", response_model=BookInDB)
async def update_book(book_id: str, book: Book):
    """
    Update an existing book in the database.

    Args:
        book_id (str): The ID of the book to update.
        book (Book): The updated book details.

    Returns:
        BookInDB: The updated details of the book.

    Raises:
        HTTPException: If the book with the given ID does not exist.

    Example Response:
    {
        "id": "string",
        "title": "string",
        "author": "string",
        "description": "string"
    }
    """
    result = db["books"].update_one({"_id": ObjectId(book_id)}, {"$set": book.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, **book.dict()}

@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    """
    Delete a book from the database.

    Args:
        book_id (str): The ID of the book to delete.

    Returns:
        dict[str, str]: A confirmation message indicating successful deletion.

    Raises:
        HTTPException: If the book with the given ID does not exist.

    Example Response:
    {
        "message": "Book deleted successfully"
    }
    """
    result = db["books"].delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
