from flask import Blueprint, render_template
from . import date_with_day_suffix, Post

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/")
def hello_world():
    return render_template("home.html")

@bp.route("/test")
def test():
    posts = Post.query.all()
    for post in posts:
        post.pub_date_str = date_with_day_suffix(post.pub_date)
    return render_template("posts.html", posts = posts)