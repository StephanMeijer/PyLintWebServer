import os
import shutil
import tempfile
from git import Repo, Git
from github import Github
from pylint_runner import lint_to_text

def getTempFolder():
    tmp = os.path.join(tempfile.gettempdir(), str(os.times()[-1]))
    os.makedirs(tmp)
    return tmp

class GitHandler(object):
    def __init__(self, data, module):
        self.__number = data['number'],
        self.__repo = data['pull_request']['head']['repo'],
        self.__branch = data['pull_request']['head']['ref'],
        self.__commit = data['pull_request']['head']['sha']
        self.__path = None
        self.__module = module

    def clone(self):
        self.__path = getTempFolder()
        Repo.clone_from(self.__repo['clone_url'], self.__path)
        Git(self.__path).checkout(self.__branch)
        Repo(self.__path).commit(self.__commit)

    def pylint_and_comment(self, config):
        """ Run the cloned repo through pylint, and comment on the PR with
        the results """
        [repo_owner, repo_name] = self.__repo['full_name'].split('/')
        path = os.path.join(self.__path, config['module'])
        gihu = Github(config['auth']['username'],
                      config['auth']['password'])
        gihu.get_user(
            repo_owner).get_repo(
                repo_name).get_issue(
                    self.__number).create_comment(
                        '**pylint results:**\n\n```\n{0}\n```'.format(
                            lint_to_text(path)))
        shutil.rmtree(path, ignore_errors=True)
