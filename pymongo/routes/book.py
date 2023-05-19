from fastapi import APIRouter,Query,HTTPException
from models.book import Book
from config.db import conn
from schema.book import bookEntity,booksEntity
from bson import ObjectId

# instantiating APIRouter class
book=APIRouter()

# endpoint to get all books
@book.get('/books')
async def get_all_books():
    try:
        return booksEntity(conn.local.books.find())
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}

# endpoint to save book to database
@book.post('/books')
async def save_book(book:Book):
    try:
        conn.local.books.insert_one(dict(book))
        return booksEntity(conn.local.books.find())
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}

# endpoint to get book by id
@book.get('/books/{id}')
async def get_book_by_id(id):
    try:
        return bookEntity(conn.local.books.find_one({"_id":ObjectId(id)}))
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")

# endpoint to update book by id
@book.put("/books/{id}")
async def update_book_by_id(id,book:Book):
    try:
        conn.local.books.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(book)})
        return {"message":"Record updated successfully"}
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}
    
# endpoint to delete book by id
@book.delete("/books/{id}")
async def delete_book_by_id(id):
    
    try:
        book = conn.local.books.find_one_and_delete({"_id": ObjectId(id)})
        if book:
            return {"message": "Record deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except HTTPException:
        raise  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# endpoin to search book by query parameters
@book.get("/search")
async def search_book(title: str = Query(None),author: str = Query(None),min_price: int = Query(None),max_price: int = Query(None)):
    # query parameters
    query = {}
    
    if title:
        query["title"] = title
    if author:
        query["author"] = author
    if min_price is not None:
        query["price"] = {"$gte":min_price}
    if max_price is not None:
        query["price"] = {"$lte":max_price}
    try:
        return booksEntity(conn.local.books.find(query))
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))

# endpoint to get total count of books
@book.get("/total_books")
async def count():
    # mongodb pipeline
    total_books_pipeline = [
        { "$count": "total_books" }
    ]
    # Execute the aggregation pipelines
    total_books_result = list(conn.local.books.aggregate(total_books_pipeline))
    # Extract the counts and book/author data from the aggregation results
    total_books = total_books_result[0]["total_books"] if total_books_result else 0
    return {"total_books": total_books}

# endpoint to get top 5 selling books
@book.get("/top_5_books")
async def top_5_books():
    # mongodb pipeline
    top_5_books_pipeline = [
        { "$sort": { "sales": -1 } },
        { "$limit": 5 },
        { "$project": { "_id": 0 } } 
    ]
    top_5_books_result = list(conn.local.books.aggregate(top_5_books_pipeline))
    top_5_books = [book for book in top_5_books_result]
    return {"top_5_bestselling_books": top_5_books}

# endpoint to get top 5 authors based on books in stock
@book.get("/top_5_authors_based_on_stocks")
async def top_5_authors():
    # mongodb pipeline
    top_5_authors_pipeline = [
        { "$group": { "_id": "$author", "total_stock": { "$sum": "$stock" } } },
        { "$sort": { "total_stock": -1 } },
        { "$limit": 5 }
    ]
    top_5_authors_result = list(conn.local.books.aggregate(top_5_authors_pipeline))
    top_5_authors = []
    for result in top_5_authors_result:
        author = result["_id"]
        total_stock = result["total_stock"]
        top_5_authors.append({"author": author, "total_stock": total_stock})

    return {"top_5_authors": top_5_authors}