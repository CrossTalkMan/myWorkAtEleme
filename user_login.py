import sqlite3
import getpass

LOGIN_TIME = 3
IS_LOGIN = False

conn = sqlite3.connect('tun_social_app')
c = conn.cursor()

count = 0
result = []

while count < LOGIN_TIME:
    name = input('plz input name:')
    password = getpass.getpass('plz input password')
    c.execute("""SELECT * FROM login_message WHERE name = ? AND password = ?""", (name, password))
    result = c.fetchall()
    if not result:
        print('wrong combination between name and password, plz check')
        count += 1
    else:
        break

if not result:
    print('plz ask administrator for help')

else:
    print(result)
    IS_LOGIN = True
