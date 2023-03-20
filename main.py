from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

error_message = str("Book not found!")
delete_message = str("The book has been deleted from the library.")

app = FastAPI()

class Book(BaseModel):
    id: str
    title : str
    ISBN: int 
    author: str
    genre: str | None = None
    pages: int 


library = {
    "FirstBook" : {"id" : "book1", "title": "FirstBook", "ISBN" : 10, "author" : "me", "genre": None, "pages" : 100},
    "SecondBook": {"id" : "book2", "title": "SecondBook", "ISBN" : 20, "author" : "me", "genre": None, "pages" : 200},
    "ThirdBook" : {"id" : "book3", "title": "ThirdBook", "ISBN" : 30, "author" : "me", "genre": None, "pages" : 300},
 }


@app.get("/view_register/{title}", response_model=Book)
async def read(title: str):
    if title not in library:
        raise HTTPException(status_code=404, detail=error_message)
    return library[title]


@app.post("/new_register/")
async def create(new_book: Book):
    if new_book.title in library:
        raise HTTPException(status_code=403, detail="Book already in library, if you want to update it go to /update_register/title.")
    new_book_encoded = jsonable_encoder(new_book)
    library[new_book.title] = new_book_encoded
    return library[new_book.title]


@app.put("/update_register/{title}", response_model=Book)
async def update(title: str, item: Book):
    if title not in library:
        raise HTTPException(status_code=404, detail=error_message)
    update_item_encoded = jsonable_encoder(item)
    library[title] = update_item_encoded
    return library[title]


@app.delete("/delete_register/{title}")
async def remove(title: str):
    if title not in library:
        raise HTTPException(status_code=404, detail=error_message)
    del library[title]
    return delete_message