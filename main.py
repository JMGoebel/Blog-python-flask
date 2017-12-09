from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog_app_user:f1nc53pM6fz0apb7ms@jasongoebel.com:3306/blog_app_db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    body = db.Column(db.String(20000), nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body

def is_valid(field):
    if field == '':
        return "<-- This field is required."

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    errors = {}

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']

        if is_valid(post_title):  errors['title'] = is_valid(post_title)
        if is_valid(post_body):  errors['body'] = is_valid(post_body)

        if len(errors) > 0:
            return render_template('newpost.html', location="New Post",  title=post_title, body=post_body, errors=errors)

        new_post = Blog(post_title, post_body)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/blog')

    return render_template('newpost.html', location="New Post", errors=errors)

@app.route('/blog')
def blog():
    posts = Blog.query.all()
    return render_template('blog.html', location="All Post", posts=posts)

if __name__ == '__main__':
    app.run()