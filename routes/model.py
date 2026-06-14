from pydantic import BaseModel, EmailStr
from typing import Literal

class Book(BaseModel):
    title: str
    author: str
    genre: Literal['Fiction', 'Non-Fiction', 'Science', 'Other']

class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: Literal['Fiction', 'Non-Fiction', 'Science', 'Other'] | None = None

class Member(BaseModel):
    name: str
    email: EmailStr

class UpdateMember(BaseModel):
    name: str | None = None
    email: EmailStr | None = None