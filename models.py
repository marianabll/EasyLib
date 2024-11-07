from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List

# Helper para lidar com ObjectId no Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class TransactionModel(BaseModel):
    transaction_type: str
    transaction_date: str
    user_id: str

class UserModel(BaseModel):
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: str = None  # Este campo será gerado automaticamente pelo MongoDB
    username: str
    email: str
    full_name: str
    date_of_birth: str
    join_date: str
    is_active: bool
    favorite_genres: List[str]
    transactions: List['TransactionModel'] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class BookModel(BaseModel):
    id: str = None
    book_name: str
    author: dict
    publisher: str
    release_year: int
    book_genre: str
    pages: int
    isbn: str
    summary: str
    average_rating: float
    tags: list[str]
    transactions: list[TransactionModel] = []
