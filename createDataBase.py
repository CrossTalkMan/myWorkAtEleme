import sqlite3

conn = sqlite3.connect('tun_social_app')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS login_message
            (id int UNIQUE primary key,
            name text,
            password text)""")
c.execute("""INSERT INTO login_message VALUES (0, 'a', 'aaa')""")
c.execute("""INSERT INTO login_message VALUES (1, 'b', 'bbb')""")
c.execute("""INSERT INTO login_message VALUES (2, 'c', 'ccc')""")

conn.commit()
conn.close()