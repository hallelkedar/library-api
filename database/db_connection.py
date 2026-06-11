import mysql.connector
from secret import DB_PASSWORD

class DBconnection:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def create_tables(self):

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                        id INT AUTO_INCERMENT PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        author VARCHAR(50) NOT NULL,
                        genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
                        is_available BOOLEAN NOT NULL,
                        borrowed_by_member_id INT UNIQUE
                        );
                ''')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS members (
                        id INT AUTO_INCERMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        is_active BOOLEAN NOT NULL,
                        total_borrows INT AUTO_INCREMENT NOT NULL
                    );
                    ''')
        self.conn.commit()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

db_connection = DBconnection(host='localhost',
                    user='root', 
                    password=DB_PASSWORD,
                    database='library_db'
                    )