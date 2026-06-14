from database.basemodel_db import BaseModel

class MemberDB(BaseModel):
    def __init__(self, table_name='members'):
        super().__init__(table_name=table_name)

    def find_in_table(self, column: str, value):
        conn = self.db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                f'SELECT * FROM {self.table_name} WHERE {column} = %s', (value,))
            return cursor.fetchall()
        
    def create_member(self, data: dict) -> int:
        member = data.copy()
        member['is_active'] = True
        member['total_borrows'] = 0
        
        if not self.find_in_table('email', member['email']):
            new_id = super().create_item(member)
            return new_id
    
    def get_all_members(self) -> list[dict]:
        return super().get_all_items()
    
    def get_member_by_id(self, member_id: int) -> dict | None:
        return super().get_item_by_id(member_id)
    
    def update_member(self, member_id: int, data: dict) -> bool:
        return super().update_item(member_id, data)
    
    def delete_member(self, member_id: int) -> bool:
        return super().delete_item(member_id)
    
    def deactivate_member(self, member_id: int) -> bool:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
                UPDATE {self.table_name}
                SET is_active = False
                WHERE id = %s
                '''
            cursor.execute(query, (member_id,))
            conn.commit()

            changed = cursor.rowcount > 0
            return changed
        
    def activate_member(self, member_id: int) -> bool:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
                UPDATE {self.table_name}
                SET is_active = True
                WHERE id = %s
                '''
            cursor.execute(query, (member_id,))
            conn.commit()
            changed = cursor.rowcount > 0
            return changed
        
    def incerment_borrows(self, member_id: int) -> bool:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
                UPDATE {self.table_name}
                SET total_borrows = total_borrows + 1
                WHERE id = %s
                '''
            cursor.execute(query, (member_id,))
            conn.commit()
            changed = cursor.rowcount > 0
            return changed
        
    def count_active_members(self) -> int:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = f'''
                SELECT COUNT(*) AS COUNT
                FROM {self.table_name}
                WHERE is_active = TRUE
                '''
            cursor.execute(query)
            active_count = cursor.fetchone()['COUNT']
            return active_count if active_count else 0
        
    def get_top_member(self) -> dict | list[dict]:
        conn = self.db.get_connection()
        with conn.cursor(dictionary=True) as cursor:
            qeury = f'''
                    SELECT id AS member_id, total_borrows AS borrowed
                    FROM {self.table_name}
                    WHERE total_borrows = (
                        SELECT MAX(total_borrows) 
                        FROM {self.table_name}
                        )
                    '''
            cursor.execute(qeury)
            return cursor.fetchall()
        