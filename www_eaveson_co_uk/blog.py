from flask import Blueprint, render_template, request, redirect, url_for
from www_eaveson_co_uk.functions import date_with_day_suffix
from www_eaveson_co_uk.database import db
from datetime import datetime
import markdown
from www_eaveson_co_uk.auth import login_required

bp = Blueprint('blog', __name__)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    live = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

@bp.route("/")
def posts():
    posts = Post.query.all()
    for post in posts:
        post.body = markdown.markdown(post.body, extensions=['extra', 'codehilite'])
        post.pub_date_str = date_with_day_suffix(post.pub_date)
    return render_template("blog/posts.html", posts = posts)

@bp.route("/add", methods =('GET','POST'))
@login_required
def add():
    if request.method == 'POST':
        body = request.form['body']
        post = Post(body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.posts'))
    return render_template('blog/edit.html')

@bp.route("/edit/<int:post_id>", methods = ('GET', 'POST'))
@login_required
def edit(post_id):
    if request.method == 'POST':
        body = request.form['body']
        post = Post.query.filter_by(id=post_id).first()
        post.body = body
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.posts'))
    post = Post.query.filter_by(id=post_id).first()
    return render_template('blog/edit.html', post=post)

@bp.route("/delete/<int:post_id>")
@login_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.posts'))