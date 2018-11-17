import hashlib

# import the Flask class from the flask module
import hmac

import os
from flask import Flask, request

from add_work_log_helper import log_work_on_jira


# create the application object
app = Flask(__name__)

GITHUB_SECRET_TOKEN = os.getenv('GITHUB_SECRET_TOKEN')


@app.route('/')
def home():
    return "Github webhook to automatically log work on JIRA from git pushes"  # render a template


@app.route('/payload', methods=['POST'])
def github_webhook():
    if not _is_authentic(request):
        return "Signature Authentication Failed"

    data = request.get_json()
    commits = data.get('commits', [])
    branch_name = data["ref"]
    for commit in commits:
        msg = commit["message"]
        log_work_on_jira(branch_name, msg)
    return "Completed"


def _is_authentic(request):
    digest = hmac.new(GITHUB_SECRET_TOKEN.encode(), request.data, hashlib.sha1).hexdigest()
    sig_parts = request.headers.get('X-Hub-Signature').split('=', 1) if request.headers.get('X-Hub-Signature') else None
    print(sig_parts)
    print(digest)
    # if len(sig_parts) < 2 or sig_parts[0] != 'sha1' or not hmac.compare_digest(sig_parts[1], digest):
    #     return False
    # return True
    return True


# start the server with the 'run()' method
if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
