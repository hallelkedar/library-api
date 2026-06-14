from fastapi import HTTPException
from services.app_service import book_db
from services import member_service
from logs.logger import logger

def get_all_books():
    all_books = book_db.get_all_books()
    if not all_books:
        logger.warning('Books list is empty.')
    return all_books

def get_book(book_id: int) -> dict | None:
    book = book_db.get_book_by_id(book_id)
    if not book:
        raise HTTPException(404, 'Book not found.')
    return book

def valid_borrow(book_id: int, member_id: int) -> dict | None:
    book = get_book(book_id)
    member = member_service.get_member(member_id)
    
    if book_db.count_active_borrows_by_member(member_id) > 3:
        raise HTTPException(400, 'Member has reached maximum borrows')
    
    if not book['is_available']:
        raise HTTPException(400, 'Book is not available')
    
    if not member['is_active']:
        raise HTTPException(400, 'Member is not active')

    return book

def valid_return(book_id: int, member_id: int) -> dict | None:
    book = get_book(book_id)
    member = member_service.get_member(member_id)
    
    if book['is_available']:
        raise HTTPException(400, 'Book is not borroewd')
    
    if book['borrowed_by_member_id'] != member_id:
        raise HTTPException(400, 'Book is not borrowed by this member')
    
    if not member['is_active']:
        raise HTTPException(400, 'Member is not active')

    return book