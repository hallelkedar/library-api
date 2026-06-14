# Library-api
## Library manager system, split into books, members and reports - routes.

**run with FastAPI server that gets http requests,
process,
and connect with SQL db (library_db - books table and members table)**

Docker run (change password to yours) -
```
docker run --name mysql-w10 -e MYSQL_ROOT_PASSWORD=<your_password> -e MYSQL_DATABASE=library -p 3306:3306 -d mysql:8
```

Direction structure -
```
library-api/
│
│
├── main.py
├── database/
│   ├── basemodel_db.py
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── model.py
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   ├── logger.py
│   └── app.log
├── services/
│   ├── app_service.py
│   ├── book_service.py
│   ├── member_service.py
│   └── reports_service.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## === Tables ===

### books:
```
id - primary key,
title - 50 chars max (not null),
author - 50 chars max (not null),
genre - Fiction / Non-fiction / Science / History / Other (must be in this list!)
is_available - True / False (not null),
borrowed_by_member_id - if borrowed, borrow member id
```

### members:
```
id - primary key,
name - 50 chars max (not null)
email - uniqe mail address (not null)
is_active - True / False (not null)
total_borrows - sum of borrows (not null)
```

## === Rules ===
1. _book creation_ - **user** send - title, author, genre, **system** add - is_available=True, borroqed_by=NULL

2. _genre_  - Must be - Fiction / Non-Fiction / Science / History / Other, else - return error (in POST/PUT/PATCH)

3. _member creation_ - **user** send - name, email, **system** add - is_active=True, total_borrows=0

4. _email_ - Must be uniqe. else return error.

5. _deactive member_ - Can't borrow book if is_active=False

6. _not available book_ - Can't borrow book if is_available=False (already borrow)

7. _maximum books_ - Members can't hold more than 3 books at time

8. _book return_ - Member can return book only if it's borrowed to him

## === EndPoints ===

### Books:
```
POST - /books - Create book
GET - /books - Get all books
GET - /books/{id} - Get book
PATCH - /books/{id} - Update book
PATCH - /books/{id}/borrow/{member_id} - Book borrow to member
PATCH - /books/{id}/return/{member_id} - Book return from member
```

### Members:
```
POST - /members - Create member 
GET - /members - Get all members
GET - /members/{id} - Get member
PATCH - /members/{id} - Update member
PATCH - /members/{id}/deactivate - Deactive member
PATCH - /members/{id}/activate - Activate member
```

### Reports:
```
GET - /reports/summary - Return general summery
GET - /reports/books-by-genre - Return books by genre stat
GET - /reports/top-member - Return most active member
```

## === System Flow ===
user -> server/endpoint -> proccess the request -> connect to database -> return the result -> server send result (or raise error)

## RUN WITH:

install requirements moduls:
```
pip install -r requirements.txt
```

run server:
```
uvicorn main:app
```