import sqlite3

def save_debate_to_db(debate_id, topic, ip_address, pro_args, con_args):
        conn = sqlite3.connect("debates.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS debates
                          (debate_id TEXT PRIMARY KEY, topic TEXT, ip_address TEXT, pro_args TEXT, con_args TEXT)''')

        cursor.execute("INSERT INTO debates (debate_id, topic, ip_address, pro_args, con_args) VALUES (?, ?, ?, ?, ?)",
                       (debate_id, topic, ip_address, pro_args, con_args))

        conn.commit()
        conn.close()