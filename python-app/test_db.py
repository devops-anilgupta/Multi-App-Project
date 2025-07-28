import mysql.connector

conn = mysql.connector.connect(
    host='mysql-db',
    user='root',
    password='password',
    database='userdb'
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")
print(cursor.fetchall())  # should show [('users',)] if init.sql ran successfully

cursor.close()
conn.close()
