from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
import git
import hmac
import hashlib
import json
import os
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

db = SQLAlchemy()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

def date_with_day_suffix(date: date) -> str:
    """
    Give the function a date object and a string will be
    returned with the date in day, month year format but
    the day will have the correct suffix added like 1st,
    2nd, 3rd, 4th etc...
    an example use would be:
    test_date = date(2023,1,22)
    a = date_with_day_suffix(test_date)
    print(a)
    22nd January 2023
    """
    day = date.strftime("%d").lstrip("0")
    if day[-1] == "1":
        day = day + "st"
    elif day[-1] == "2":
        day = day + "nd"
    elif day[-1] == "3":
        day = day + "rd"
    else:
        day = day + "th"
    return f"{day} {date.strftime('%B %Y')}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/test")
def test():
    posts = Post.query.all()
    for post in posts:
        post.pub_date_str = date_with_day_suffix(post.pub_date)
    return render_template("posts.html", posts = posts)

def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method != 'POST':
        return 'OK'
    else:
        abort_code = 418
        # Do initial validations on required headers
        if 'X-Github-Event' not in request.headers:
            abort(abort_code)
        if 'X-Github-Delivery' not in request.headers:
            abort(abort_code)
        if 'X-Hub-Signature' not in request.headers:
            abort(abort_code)
        if not request.is_json:
            abort(abort_code)
        if 'User-Agent' not in request.headers:
            abort(abort_code)
        ua = request.headers.get('User-Agent')
        if not ua.startswith('GitHub-Hookshot/'):
            abort(abort_code)


        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'})
        if event != "push":
            return json.dumps({'msg': "Wrong event type"})

        x_hub_signature = request.headers.get('X-Hub-Signature')
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        if not is_valid_signature(x_hub_signature, request.data, WEBHOOK_SECRET):
            print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
            abort(abort_code)

        payload = request.get_json()
        if payload is None:
            print('Deploy payload is empty: {payload}'.format(
                payload=payload))
            abort(abort_code)

        if payload['ref'] != 'refs/heads/main':
            return json.dumps({'msg': 'Not main; ignoring'})

        repo = git.Repo('/home/Ceaveson/mysite/www.eaveson.co.uk')
        origin = repo.remotes.origin
        origin.pull()

        pull_info = origin.pull()

        if len(pull_info) == 0:
            return json.dumps({'msg': "Didn't pull any information from remote!"})
        if pull_info[0].flags > 128:
            return json.dumps({'msg': "Didn't pull any information from remote!"})

        commit_hash = pull_info[0].commit.hexsha
        build_commit = f'build_commit = "{commit_hash}"'
        print(f'{build_commit}')
        return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash)