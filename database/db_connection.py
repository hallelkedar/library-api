import mysql.connector
from secret import DB_PASSWORD

class DBconnection:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        
        self.conn = None
        self.connect()
    
    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )

    def get_connection(self):
        if not self.conn.is_connected() or self.conn is None:
            self.connect()
        return self.conn
    
    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS library')
        cursor.execute('USE library')
        cursor.close()

    def init_tables(self):
        
        cursor = self.conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        author VARCHAR(50) NOT NULL,
                        genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
                        is_available BOOLEAN NOT NULL,
                        borrowed_by_member_id INT UNIQUE
                        );
                ''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS members (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        is_active BOOLEAN NOT NULL,
                        total_borrows INT NOT NULL
                    );
                    ''')
        cursor.close()

    def close_db(self):
        self.conn.close()

db_connection = DBconnection(host='localhost',
                    user='root', 
                    password=DB_PASSWORD
                    )