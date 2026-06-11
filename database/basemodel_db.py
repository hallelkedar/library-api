from db_connection import db_connection
from secret import DB_PASSWORD

class BaseModel:
    def __init__(self, table_name):
        self.table_name = table_name
        self.db = db_connection

    def get_all_items(self) -> list[dict]:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f'SELECT * FROM {self.table_name}')
            
            books = cursor.fetchall()
            return books
    
    def get_item_by_id(self, message_id: int) -> dict | None:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'SELECT * FROM {self.table_name} WHERE id = %s'
            cursor.execute(query, (message_id,))

            item = self.cursor.fetchone()
            return item
    
    def create_item(self, data: dict) -> int:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            columns = ', '.join(data)
            placeholders = ', '.join(['%s'] * len(data))

            query = f'INSERT INTO {self.table_name} ({columns} VALUES ({placeholders}))'
            params = tuple(data.values())

            cursor.execute(query, params)
            self.conn.commit()

            new_id = cursor.lastrowid
            return new_id
    
    def update_item(self, item_id: int, data: dict) -> bool:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            set_clause = [f'{key} = %s' for key in data]

            query = f'UPDATE {self.table_name} SET ({set_clause}) WHERE id = %s'
            params = list(data.values()) + [item_id]

            cursor.execute(query, params)
            self.conn.commit()

            changed = cursor.rowcount > 0
            return changed
    
    def delete_item(self, item_id: int) -> bool:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'DELETE FROM {self.table_name} WHERE id = %s'
            
            cursor.execute(query, (item_id,))
            self.conn.commit()

            changed = cursor.rowcount > 0
            return changed