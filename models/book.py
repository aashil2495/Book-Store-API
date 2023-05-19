from pydantic import BaseModel,Field

# Book class for storing book fields with validations
class Book(BaseModel):
    title: str=Field(...,min_length=1,max_length=50)
    author:str=Field(...,min_length=1,max_length=50)
    description:str=Field(...,min_length=1,max_length=50)
    price:int=Field(...,gt=0)
    stock:int=Field(...,gt=0)
    sales:int=Field(...)