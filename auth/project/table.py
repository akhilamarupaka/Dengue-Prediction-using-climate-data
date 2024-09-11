import sqlite3

conn = sqlite3.connect('loc.db')

c = conn.cursor()

c.execute("""INSERT INTO loc values(17.4009, 78.4965,0)""")
c.execute("""INSERT INTO loc values(17.4009, 78.4965,1)""")
c.execute("""INSERT INTO loc values(17.4009, 78.4965,1)""")

conn.commit()
conn.close()