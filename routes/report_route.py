from fastapi import APIRouter
from services.app_service import book_db, member_db
from services import reports_service

router = APIRouter()

@router.get('/summery')
def get_report_summery():
    return reports_service.summery_report()

@router.get('/books-by-genre')
def get_books_by_genre():
    return book_db.count_by_genre()

@router.get('/top-member')
def get_top_member():
    return member_db.get_top_member()