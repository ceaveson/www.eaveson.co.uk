import os
from flask import Flask, request, abort, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import json
import git
from www_eaveson_co_uk.functions import is_valid_signature, date_with_day_suffix
from www_eaveson_co_uk import auth, blog

load_dotenv() 

DATABASE_URI = os.getenv('DATABASE_URI')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY')


def create_app(test_config=None):
    db = SQLAlchemy()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = SECRET_KEY,
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    return app

#db = SQLAlchemy(app)

    # @app.route('/update_server', methods=['POST'])
    # def webhook():
    #     if request.method != 'POST':
    #         return 'OK'
    #     else:
    #         abort_code = 418
    #         # Do initial validations on required headers
    #         if 'X-Github-Event' not in request.headers:
    #             abort(abort_code)
    #         if 'X-Github-Delivery' not in request.headers:
    #             abort(abort_code)
    #         if 'X-Hub-Signature' not in request.headers:
    #             abort(abort_code)
    #         if not request.is_json:
    #             abort(abort_code)
    #         if 'User-Agent' not in request.headers:
    #             abort(abort_code)
    #         ua = request.headers.get('User-Agent')
    #         if not ua.startswith('GitHub-Hookshot/'):
    #             abort(abort_code)


    #         event = request.headers.get('X-GitHub-Event')
    #         if event == "ping":
    #             return json.dumps({'msg': 'Hi!'})
    #         if event != "push":
    #             return json.dumps({'msg': "Wrong event type"})

    #         x_hub_signature = request.headers.get('X-Hub-Signature')
    #         # webhook content type should be application/json for request.data to have the payload
    #         # request.data is empty in case of x-www-form-urlencoded
    #         if not is_valid_signature(x_hub_signature, request.data, WEBHOOK_SECRET):
    #             print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
    #             abort(abort_code)

    #         payload = request.get_json()
    #         if payload is None:
    #             print('Deploy payload is empty: {payload}'.format(
    #                 payload=payload))
    #             abort(abort_code)

    #         if payload['ref'] != 'refs/heads/main':
    #             return json.dumps({'msg': 'Not main; ignoring'})

    #         repo = git.Repo('/home/Ceaveson/mysite/www.eaveson.co.uk')
    #         origin = repo.remotes.origin
    #         origin.pull()

    #         pull_info = origin.pull()

    #         if len(pull_info) == 0:
    #             return json.dumps({'msg': "Didn't pull any information from remote!"})
    #         if pull_info[0].flags > 128:
    #             return json.dumps({'msg': "Didn't pull any information from remote!"})

    #         commit_hash = pull_info[0].commit.hexsha
    #         build_commit = f'build_commit = "{commit_hash}"'
    #         print(f'{build_commit}')
    #         return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash)