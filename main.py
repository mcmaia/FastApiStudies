from fastapi import FastAPI
from pydantic import BaseModel, Field

from typing import Optional


app = FastAPI()

# a class to get the book
class Book:
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: int
    
    def __init__(self, id, title, author, category, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.description = description
        self.rating = rating

# a class to get the book request       
class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=3)
    author: str = Field(..., min_length=3)
    category: str  = Field(..., min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=0, le=6)

    
# a list of books
BOOKS = [
    Book(1, "The Catcher in the Rye", "J.D. Salinger", "Fiction", "A classic novel about teenage angst", 4),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Fiction", "A story of racial injustice in the American South", 5),
    Book(3, "1984", "George Orwell", "Science Fiction", "A dystopian novel set in a totalitarian society", 4),
    Book(4, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "A tale of the Jazz Age and the American Dream", 4),
    Book(5, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", "The first book in the Harry Potter series", 5),
]

# a function to get all books
@app.get("/books")
async def read_all_books():
    return BOOKS

# a function to get a book by id
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(automate_book_id(new_book))
    return book_request

#a function to automate the book id
def automate_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book