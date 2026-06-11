from db_connection import db_connection
from secret import DB_PASSWORD

class BaseModel:
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = db_connection
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all_items(self) -> list[dict]:
        self.cursor.execute('SELECT * FROM %s', (self.table_name,))
        
        books = self.cursor.fetchall()
        return books
    
    def get_item_by_id(self, message_id: int) -> dict | None:
        query = f'SELECT * FROM {self.table_name} WHERE id = %s'
        self.cursor.execute(query, (message_id,))

        item = self.cursor.fetchone()
        return item
    
    def create_item(self, data: dict) -> int:
        columns = ', '.join(data)
        placeholders = ', '.join(['%s'] * len(data))

        query = f'INSERT INTO {self.table_name} ({columns} VALUES ({placeholders}))'
        params = tuple(data.values())

        self.cursor.execute(query, params)
        self.conn.commit()

        new_id = self.cursor.lastrowid
        return new_id
    
    def update_item(self, item_id: int, data: dict) -> bool:
        set_clause = [f'{key} = %s' for key in data]

        query = f'UPDATE {self.table_name} SET ({set_clause}) WHERE id = %s'
        params = list(data.values()) + [item_id]

        self.cursor.execute(query, params)
        self.conn.commit()

        changed = self.cursor.rowcount > 0
        return changed
    
    def delete_item(self, item_id: int) -> bool:
        query = f'DELETE FROM {self.table_name} WHERE id = %s'
        
        self.cursor.execute(query, (item_id,))
        self.conn.commit()

        changed = self.cursor.rowcount > 0
        return changed