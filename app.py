from flask import Flask, render_template, request
import git

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/ceaveson/www.eaveson.co.uk')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400