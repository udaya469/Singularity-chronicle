
from flask import Flask,render_template, request, url_for, flash, redirect
import sqlite3


app = Flask(__name__)



def connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app.config['SECRET_KEY'] ='fc311aecf1a50dc92997152bdde07cc5564716a2a05700e0'
def get_data():
        conn = connection()
        blog_posts = conn.execute('SELECT * FROM posts').fetchall()
        conn.close()
        return blog_posts

@app.route('/')
@app.route('/index/')
def index():
        return render_template('intro.html')

@app.route('/blogs/')
def blogs():
        blog_posts = get_data()
        return render_template('blogs.html',blogs=blog_posts)



@app.route('/blogs/<url>/')
def blog(url):
        blog_posts = get_data()
        for blog in blog_posts:
                if blog['url'] == url:
                        return render_template('blog.html',blog=blog)

@app.route('/create/',methods=('GET','POST'))
def create():
    if request.method == 'POST':
       title = request.form['title'].upper()
       url = request.form['url']
       content = request.form['content']

       if not title:
           flash('Title is required!')
       elif not url:
           flash('URL is required!')
       elif not content:
           flash('Content is required!')
       else:
           conn = connection()
           cursor = conn.execute('SELECT COUNT(*) FROM posts WHERE url = ?', (url,))
           count = cursor.fetchone()[0]

           if count > 0:
                flash('Error: URL already exists!')
           else:
                conn.execute('INSERT INTO posts (title, url, content) VALUES (?, ? ,?)',
                        (title, url, content))
                conn.commit()
                conn.close()
                return redirect(url_for('blogs'))

    return render_template('blog/create.html')

@app.route('/blogs/<url>/edit/', methods=['GET', 'POST'])
def edit(url):
    conn = connection()

    if request.method == 'POST':
        new_title = request.form['new_title'].upper()

        new_content = request.form['new_content']

        if not new_title:
            flash('Title is required!')
        elif not new_content:
            flash('Content is required!')
        else:
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE url = ?', (new_title, new_content, url))
            conn.commit()
            conn.close()
            flash('Blog Updated!')
            return redirect(url_for('blogs'))

    blog = conn.execute('SELECT * FROM posts WHERE url = ?', (url,)).fetchone()
    conn.close()
    return render_template('blog/edit.html', blog=blog)

@app.route('/blogs/<url>/delete/', methods=['POST'])
def delete_blog(url):
    conn = connection()
    conn.execute('DELETE FROM posts WHERE url = ?', (url,))
    conn.commit()
    conn.close()
    return redirect(url_for('blogs'))