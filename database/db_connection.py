import mysql.connector
from secret import DB_PASSWORD

class DBconnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        self.conn = self.connect()
    
    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_connection(self):
        if self.conn.is_connected():
            return self.conn
        else:
            self.conn = self.connect()
            return self.conn
        
    def create_tables(self):
        
        cursor = self.conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                        id INT AUTO_INCERMENT PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        author VARCHAR(50) NOT NULL,
                        genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
                        is_available BOOLEAN NOT NULL,
                        borrowed_by_member_id INT UNIQUE
                        );
                ''')
        cursor.execute('''
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
        self.conn.close()

db_connection = DBconnection(host='localhost',
                    user='root', 
                    password=DB_PASSWORD,
                    database='library_db'
                    )