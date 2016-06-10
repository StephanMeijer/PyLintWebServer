from http.server import BaseHTTPRequestHandler
from github import Github
import json
import os
import shutil

from git_handler import GitHandler
from pylint_runner import lint_to_text

class GithubWebHookServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(GithubWebHookServer,self).__init__(*args, **kwargs)
        with open('config.json') as configfile:
            self.config = json.load(configfile)


    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        # TODO: authentication

        try:
            length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(length).decode('utf-8'))

            if post_data["action"] != "opened": return

            number = post_data["number"]

            clone_url = post_data["pull_request"]["head"]["repo"]["clone_url"]
            [repo_owner, repo_name] = post_data["pull_request"]["head"]["repo"]["full_name"].split('/')
            branch = post_data["pull_request"]["head"]["ref"]
            commit = post_data["pull_request"]["head"]["sha"]

            handler = GitHandler(clone_url, branch, commit)
            handler.clone()

            path = handler.getPath()

            self.__githubRespond(path, number, repo_owner, repo_name)
        except:
            print("Something gone wrong")

    def __githubRespond(self, path, number, repo_owner, repo_name):
        path = os.path.join(path, self.config['module'])
        text = lint_to_text(path)

        gihu = Github(self.config['auth']['username'], self.config['auth']['password'])

        gihu.get_user(repo_owner).get_repo(repo_name).get_issue(number).create_comment("**pylint results:**\n\n```\n{0}\n```".format(text))

        shutil.rmtree(path, ignore_errors=True)
