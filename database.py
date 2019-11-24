import sqlite3

db_path = ":memory:"

def __init__(config):
    """Setup all the necessary tables"""
    global db_path
    db_path = config["db_path"]

    # Connect to the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create all necesarry tables 
    #c.execute('''CREATE TABLE IF NOT EXISTS users
    #         (user_id text, platform text, interactions integer)''')
    c.execute('''CREATE TABLE IF NOT EXISTS suggestions
             (user_id text, platform text, suggestion text)''')
    conn.commit()
    conn.close()

def add_suggestion(user, platform, suggestion):
    """Adds a new suggestion to the database"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO suggestions VALUES (?, ?, ?)", (user, platform, suggestion))
    conn.commit()
    conn.close() 

def get_and_clear_suggestions():
    """Returns all suggestion and also deletes the table"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    suggestions = c.execute("SELECT * FROM suggestions").fetchall()
    c.execute("DELETE FROM suggestions")
    conn.commit()
    conn.close()  

    return suggestions


