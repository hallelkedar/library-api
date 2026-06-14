from fastapi import APIRouter
from routes.model import Book, UpdateBook
from services.app_service import book_db, member_db
from services import book_service

router = APIRouter()

@router.post('')
def create_book(data: Book):
    book = data.model_dump()
    new_id = book_db.create_book(book)
    return {'detail': f'Book (-id-:{new_id}) created'}

@router.get('')
def get_all_books():
    return book_db.get_all_books()

@router.get('/{id}')
def get_book(id: int):
    return book_service.get_book(id)

@router.patch('/{id}')
def update_book(id: int, data: UpdateBook):
    data_dict = data.model_dump(exclude_unset=True)
    book_service.get_book(id)
    book_db.update_book(id, data_dict)
    
    return {'detail': f'Book (-id:{id}) updated.'}

@router.patch('/{id}/borrow/{member_id}')
def borrow_book_to_member(id: int , member_id: int):
    book = book_service.valid_borrow(id, member_id)
    book_db.set_availability(id, False, member_id)
    member_db.incerment_borrows(member_id)
    
    return {'detail': f'Member ({member_id}) borrow book ({id}) - {book['title']} by {book['author']}.'}

@router.patch('/{id}/return/{member_id}')
def return_book(id: int, member_id: int):
    book = book_service.valid_return(id, member_id)
    book_db.set_availability(id, True, None)
    
    return {'detail': f'Member ({member_id}) return book ({id}) - {book['title']} by {book['author']}.'}