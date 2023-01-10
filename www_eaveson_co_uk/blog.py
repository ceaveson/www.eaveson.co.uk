from flask import Blueprint, render_template, request, redirect, url_for
from www_eaveson_co_uk.functions import date_with_day_suffix
from www_eaveson_co_uk.database import db
from datetime import datetime
import markdown

bp = Blueprint('blog', __name__)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

@bp.route("/")
def index():
    return render_template("blog/home.html")

@bp.route("/test")
def test():
    posts = Post.query.all()
    for post in posts:
        post.body = markdown.markdown(post.body)
        post.pub_date_str = date_with_day_suffix(post.pub_date)
    return render_template("blog/posts.html", posts = posts)

@bp.route("/add", methods =('GET','POST'))
def add():
    if request.method == 'POST':
        body = request.form['body']
        post = Post(body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.test'))
    return render_template('blog/add_post.html')