from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "year": "1890", "category": "Gothic Fiction"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": "1925", "category": "Tragedy"},
    {"title": "The Catcher in the Rye", "author": "J. D. Salinger", "year": "1951", "category": "Coming-of-age Fiction"},
    {"title": "The Grapes of Wrath", "author": "John Steinbeck", "year": "1939", "category": "Realistic Fiction"},
    {"title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "year": "1884", "category": "Adventure Fiction"},
]

# dynamic path
@app.get("/books/{book_title}")
async def get_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
#query parameter
@app.get("/books/")
async def get_book_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

# dynamic path and query parameter
@app.get("/books/{book_author}/")
async def get_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return