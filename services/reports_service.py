from services.app_service import book_db, member_db

def summery_report() -> dict:
    return {
        'total_books': book_db.count_total_books(),
        'available_books': book_db.count_available_books(),
        'currently_borrowed': book_db.count_borrowed_books(),
        'active_members': member_db.count_active_members()
    }