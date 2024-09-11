import sqlite3

conn = sqlite3.connect('loc.db')

c = conn.cursor()

c.execute("""CREATE TABLE user_prof5(
            email text,
            name text,
            lat integer,
            lon integer,
            fever text,
            checked_symptoms text,
            date_time text,
            type integer
            )""")
    
conn.commit()
conn.close()
