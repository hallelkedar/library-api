from fastapi import HTTPException
from database.book_db import BookDB
from database.member_db import MemberDB

book_db = BookDB()
member_db = MemberDB()