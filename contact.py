import pymysql

# MySQL serveriga ulanish
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='users.db'
)

# Cursor ob'ektini yaratish
cursor = conn.cursor()

# Ma'lumot qo'shish
cursor.execute("INSERT INTO users (name, email) VALUES ('Diyorbek', 'diyor@example.com')")

# O'zgartirishlarni saqlash
conn.commit()

# Ma'lumotlarni tekshirish
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Yopish
conn.close()
