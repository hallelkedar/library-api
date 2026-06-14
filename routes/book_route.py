from fastapi import APIRouter
from routes.model import Book, UpdateBook, BookResponse
from services.app_service import book_db, member_db
from services import book_service
from logs.logger import logger

router = APIRouter()

@router.post('', status_code=201)
def create_book(data: Book):
    book = data.model_dump()
    new_id = book_db.create_book(book)
    return_msg = {'detail': f'Book (-id-:{new_id}) created'}
    logger.info(return_msg['detail'])
    return return_msg

@router.get('', response_model=list[BookResponse])
def get_all_books():
    all_books = book_service.get_all_books()
    logger.info('Return all books list')
    return all_books

@router.get('/{id}', response_model=BookResponse)
def get_book(id: int):
    book = book_service.get_book(id)
    logger.info(f'Return book number - {id}')
    return book

@router.patch('/{id}')
def update_book(id: int, data: UpdateBook):
    data_dict = data.model_dump(exclude_unset=True)
    book_service.get_book(id)
    book_db.update_book(id, data_dict)
    
    return_msg = {'detail': f'Book (-id:{id}) updated.'}
    logger.info(return_msg['detail'])
    return return_msg

@router.patch('/{id}/borrow/{member_id}')
def borrow_book_to_member(id: int , member_id: int):
    book = book_service.valid_borrow(id, member_id)
    book_db.set_availability(id, False, member_id)
    member_db.incerment_borrows(member_id)
    
    return_msg = {'detail': f'Member ({member_id}) borrow book ({id}) - {book['title']} by {book['author']}.'}
    logger.info(return_msg['detail'])
    return return_msg

@router.patch('/{id}/return/{member_id}')
def return_book(id: int, member_id: int):
    book = book_service.valid_return(id, member_id)
    book_db.set_availability(id, True, None)
    
    return_msg = {'detail': f'Member ({member_id}) return book ({id}) - {book['title']} by {book['author']}.'}
    logger.info(return_msg['detail'])
    return return_msg