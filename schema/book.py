# mongodb schema file will convert the fields from object format(mongodb's format) to python readable format

# single book conversion
def bookEntity(item)->dict:
    return {
        "id":str(item["_id"]),
        "title":item["title"],
        "author":item["author"],
        "description":item["description"],
        "price":str(item["price"]),
        "stock":str(item["stock"]),
        "sales":int(item["sales"])
        
    }

# all books conversion
def booksEntity(entity)->list:
    return [bookEntity(item) for item in entity]