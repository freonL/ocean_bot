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

    c.execute('''CREATE TABLE session
                    (recipient_id, session_id)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    reset_db()