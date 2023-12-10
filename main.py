from typing import Optional
from datetime import datetime

#validate Path parameters
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# a class to get the book
class Book:
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: int
    published_year: int
    
    def __init__(self, id, title, author, category, description, rating, published_year=None):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.description = description
        self.rating = rating
        self.published_year = published_year    

# a class to get the book request       
class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, title="The ID of the book", description="This ID is automatically generated")
    title: str = Field(..., min_length=3)
    author: str = Field(..., min_length=3)
    category: str  = Field(..., min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    published_year: Optional[int] = Field(default=None, le=datetime.now().year)
    rating: int = Field(ge=0, le=5) #between 1 and 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "add the author name",
                "category": "add the category",
                "description": "add the description",
                "rating": 4,
                "published_year": 2023
            }
        }
            

    
# a list of books
BOOKS = [
    Book(1, "The Catcher in the Rye", "J.D. Salinger", "Fiction", "A classic novel about teenage angst", 4, 1951),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Fiction", "A story of racial injustice in the American South", 5),
    Book(3, "1984", "George Orwell", "Science Fiction", "A dystopian novel set in a totalitarian society", 4),
    Book(4, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "A tale of the Jazz Age and the American Dream", 4),
    Book(5, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", "The first book in the Harry Potter series", 5),
]

# a function to get all books
@app.get("/books")
async def read_all_books():
    return BOOKS


#Path(gt=0) means that the book_id must be greater than 0 only for this endpoint
@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


#Query(gt=0, le=5) means that the book_rating must be greater than 0 and less than or equal to 5 only for this endpoint
@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0, le=5)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
             book_to_return.append(book)
    return book_to_return


@app.get("/books/published-year/")
async def book_by_year(published_year: int = Query(le=datetime.now().year)):
    book_to_return = []
    for book in BOOKS:
        if book.published_year == published_year:
            book_to_return.append(book)
    return book_to_return
   

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


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
            return book
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

      
@app.delete("/books/{book_id}") 
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            raise HTTPException(status_code=200, detail="Book with id: {} was deleted".format(book_id))
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book with id: {} was not found".format(book_id))
      
