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

def get_previous_debates():
        # Connect to the SQLite database
        conn = sqlite3.connect("debates.db")
        cursor = conn.cursor()

        # Execute the query to fetch previous debates
        cursor.execute("SELECT * FROM debates")

        # Fetch all the rows as a list of tuples
        previous_debates = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Return the list of previous debates
        return previous_debates