from fastapi import APIRouter
from services.app_service import book_db, member_db
from services import reports_service
from logs.logger import logger

router = APIRouter()

@router.get('/summery')
def get_report_summery():
    summery = reports_service.summery_report()
    logger.info('Return summery reports dict')
    return summery

@router.get('/books-by-genre')
def get_books_by_genre():
    count_by_genre = book_db.count_by_genre()
    logger.info('Return count by genre dict')
    return count_by_genre


@router.get('/top-member')
def get_top_member():
    top_member = member_db.get_top_member()
    if not top_member:
        logger.warning('There is no borrowes in members db')
    logger.info('Return top member dict')
    return top_member