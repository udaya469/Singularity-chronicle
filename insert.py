import sqlite3

connection = sqlite3.connect('database.db')

with open('data.sql') as f:
    connection.executescript(f.read())

blog_posts = [
    {"title": 'ARTIFICIAL INTELLIGENCE', "body": 'first blog body', "url": 'ai'},
    {"title": 'ROBOTICS', "body": 'second blog body', "url": 'rb'},
    {"title": 'ETHICAL HACKING', "body": 'third blog body', "url": 'eh'}
]

cur = connection.cursor()

for post in blog_posts:
    cur.execute("INSERT INTO posts (title, content, url) VALUES (?, ?, ?)",
                (post['title'], post['body'], post['url']))

connection.commit()
connection.close()
