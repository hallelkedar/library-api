from fastapi import APIRouter, HTTPException
from model import Book, UpdateBook
from database.book_db import BookDB

router = APIRouter()

book_db = BookDB()

@router.post('')
def create_book(data: Book):
    book = data.model_dump()
    new_id = book_db.create_book(book)
    return {'detail': f'Book (-id:{new_id}) created'}

@router.get('')
def get_all_books():
    books = book_db.get_all_books()
    return books

@router.get('/{id}')
def get_book(id: int):
    book = book_db.get_book_by_id(id)
    if not book:
        raise HTTPException(404, 'Book not found.')
    return book

@router.patch('/{id}')
def update_book(id: int, data: UpdateBook):
    data_dict = data.model_dump(exclude_unset=True)
    updated = book_db.update_book(id, data_dict)
    if not updated:
        raise HTTPException(404, 'Book not found.')
    return {'detail': f'Book (-id:{id}) updated.'}

@router.patch('/{id}/borrow/{member_id}')
def borrow_book_to_member(id: int , member_id: int):
    pass