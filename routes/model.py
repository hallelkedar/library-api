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

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Literal['Fiction', 'Non-Fiction', 'Science', 'Other']
    is_available: bool
    borrowed_by_member_id: int | None

class Member(BaseModel):
    name: str
    email: EmailStr

class UpdateMember(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class MemberResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    total_borrows: int