import sqlite3
from config import DB_NAME

def reset_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM session")

    conn.commit()
    conn.close()

def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists session
                    (recipient_id text, 
                    session_id text,
                    create_time timestamp,
                    update_time timestamp)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()