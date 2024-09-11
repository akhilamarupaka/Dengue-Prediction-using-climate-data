import sqlite3

conn = sqlite3.connect('loc.db')

c = conn.cursor()

c.execute("""CREATE TABLE profile(
            name string,
            lat integer,
            lon integer,
            checked_symptoms string,
            date_time string,
            type integer
            )""")
    
conn.commit()
conn.close()
