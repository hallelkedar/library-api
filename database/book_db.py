from database.basemodel_db import BaseModel

class BookDB(BaseModel):
    def __init__(self, table_name='books'):
        super().__init__(table_name=table_name)
    
    def create_book(self, data: dict) -> int:
        book = data.copy()
        book['is_available'] = True
        book['borrowed_by_member_id'] = None
        new_id = super().create_item(book)
        return new_id
    
    def get_all_books(self) -> list[dict]:
        return super().get_all_items()
    
    def get_book_by_id(self, book_id) -> dict | None:
        book = super().get_item_by_id(book_id)
        book['is_available'] = bool(book['is_available'])
        return book
    
    def update_book(self, book_id: int, data: dict) -> bool:
        return super().update_item(book_id, data)
    
    def set_availability(self, book_id: int, val: bool, member_id: int | None) -> bool:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
            UPDATE {self.table_name}
            SET is_available = %s, borrowed_by_member_id = %s
            WHERE id = %s
            '''
            params = (val, member_id, book_id)

            cursor.execute(query, params)
            conn.commit()

            changed = cursor.rowcount > 0
            return changed
    
    def count_total_books(self) -> int:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f'SELECT COUNT(*) AS books_count FROM {self.table_name}')
            
            books_count = cursor.fetchone()
            return books_count['books_count']
    
    def count_available_books(self) -> int:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
            SELECT COUNT(*) AS avaliable_books
            FROM {self.table_name}
            WHERE is_available = TRUE
            '''
            cursor.execute(query)
            avaliable_count = cursor.fetchone()
            return avaliable_count['avaliable_books']
    
    def count_borrowed_books(self) -> int:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
            SELECT COUNT(*)
            AS borrowed_books
            FROM {self.table_name} 
            WHERE is_available = False
            '''
            cursor.execute(query)
            borrowed_count = cursor.fetchone()['borrowed_books']
            return borrowed_count if borrowed_count else 0
    
    def count_by_genre(self) -> list:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
            SELECT genre, COUNT(genre) AS COUNT
            FROM {self.table_name}
            GROUP BY genre
            '''
            cursor.execute(query)
            genre_counts = cursor.fetchall()
            return genre_counts
        
    def count_active_borrows_by_member(self, member_id: int) -> int:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
            SELECT COUNT(*) AS COUNT
            FROM {self.table_name}
            WHERE borrowed_by_member_id = %s
            '''
            cursor.execute(query, (member_id,))
            active_count = cursor.fetchone()['COUNT']
            return active_count if active_count else 0
        