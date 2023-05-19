from fastapi import FastAPI
from routes.book import book
from config.db import conn
import pymongo

app=FastAPI()
app.include_router(book)


@app.on_event("startup")
async def create_indexes():
    
    # Creating mongodb indexes on startup of project
    conn.local.books.create_index([("title", pymongo.TEXT)])
    conn.local.books.create_index([("author", pymongo.ASCENDING)])
    conn.local.books.create_index([("price", pymongo.ASCENDING)])




