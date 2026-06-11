import mysql.connector
from secret import DB_PASSWORD

def get_connect(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    return conn


def create_tables(conn):
    
    cursor = conn.cursor()

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
    conn.commit()

def close_db(cursor, conn):
    cursor.close()
    conn.close()

