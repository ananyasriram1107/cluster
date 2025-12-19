import sqlite3

def init_db():
    conn = sqlite3.connect('db/student_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            date TEXT,
            math INT,
            reading INT,
            clicks INT,
            cluster INT
        )
    ''')
    conn.commit()
    return conn
