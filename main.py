from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from routes.book_route import router as book_route
from routes.member_route import router as member_route
from routes.report_route import router as reports_route
from logs.logger import logger
from database.db_connection import db_connection
import mysql.connector

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection.init_db()
    db_connection.init_tables()
    yield
    db_connection.close_db()

app = FastAPI(lifespan=lifespan)

@app.middleware('http')
async def middleware_logging(req: Request, call_next):
    logger.info(f'{req.method} - {req.url.path} called')
    return await call_next(req)

@app.exception_handler(HTTPException)
def handle_http_exceptions(req: Request, e: HTTPException):
    logger.error(f'{e.status_code} - {e.detail}')
    return JSONResponse(status_code=e.status_code,
                        content={'detail': e.detail})

@app.exception_handler(mysql.connector.Error)
def sql_exception_handler(req: Request, e: mysql.connector.Error):
    logger.error(f'{req.method} - {req.url.path} - {e.errno} (msg: {e.msg}', exc_info=True)
    return JSONResponse(
        content={'detail': 'Iternal server error'},
        status_code=500
        )
app.include_router(book_route, prefix='/books')
app.include_router(member_route, prefix='/members')
app.include_router(reports_route, prefix='/reports')
