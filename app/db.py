import os
import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect("db/debates.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE debates (
            debate_id TEXT PRIMARY KEY,
            topic TEXT,
            pro_args TEXT,
            con_args TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_debate_to_db(debate_id, topic, ip_address, pro_args, con_args):
        db_path = "db/debates.db"
    
        # Check if the database file exists, if not, create the database
        if not os.path.exists(db_path):
                create_database()

        conn = sqlite3.connect("db/debates.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS debates
                          (debate_id TEXT PRIMARY KEY, topic TEXT, ip_address TEXT, pro_args TEXT, con_args TEXT)''')

        cursor.execute("INSERT INTO debates (debate_id, topic, ip_address, pro_args, con_args) VALUES (?, ?, ?, ?, ?)",
                       (debate_id, topic, ip_address, pro_args, con_args))

        conn.commit()
        conn.close()

def get_previous_debates():
        db_path = "db/debates.db"

        # Check if the database file exists, if not, create the database
        if not os.path.exists(db_path):
                create_database()
        conn = sqlite3.connect("db/debates.db")
        df = pd.read_sql_query("SELECT * from debates", conn)
        conn.close()
        return df

def delete_debate_from_db(debate_id):
    conn = sqlite3.connect("db/debates.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM debates WHERE debate_id = ?", (debate_id,))
    conn.commit()
    conn.close()