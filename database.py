import sqlite3

db_path = ":memory:"

def __init__(config):
    """Setup all the necessary tables"""
    global db_path
    db_path = config["db_path"]

    # Connect to the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    #Create all necesarry tables 
    c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id text, platform text, interactions integer)''')
    c.execute('''CREATE TABLE IF NOT EXISTS suggestions
             (user_id text, platform text, suggestion text)''')
    conn.commit()
    conn.close()

def add_user(user_id, platform):
    """Adds a new user to the database"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, 1)", (user_id, platform))
    conn.commit()
    conn.close() 

def increase_interaction(user_id, platform):
    """Increase the interaction counter by 1 from the user passed to this function"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE users SET interactions = interactions + 1 WHERE user_id = ? AND platform = ?", (user_id, platform))
    changed_rows = conn.total_changes
    conn.commit()
    conn.close()

    if changed_rows == 0: 
        add_user(user_id, platform)

def get_statistic():
    """Returns 2 values, the number of users and the total interactions"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    users = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    interactions = c.execute("SELECT SUM(interactions) FROM users").fetchone()[0]
    conn.commit()
    conn.close()  

    return users, interactions

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


