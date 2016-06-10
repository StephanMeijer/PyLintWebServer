from git import Repo, Git
from github import Github
from pylint_runner import lint_to_text
import os
import shutil
import tempfile

class GitHandler(object):
    def __init__(self, number, repo, branch, commit, module):
        self.__clone_url = repo['clone_url']
        self.__branch = branch
        self.__commit = commit
        self.__path = None
        self.__number = number
        self.__module = module

    def clone(self):
        self.__path = self.__getTempFolder()
        Repo.clone_from(self.__clone_url, self.__path)
        Git(self.__path).checkout(self.__branch)
        Repo(self.__path).commit(self.__commit)

    def __getTempFolder(self):
        tmp = os.path.join(tempfile.gettempdir(), str(os.times()[-1]))
        os.makedirs(tmp)
        return tmp

    def __pylint_and_comment(self, number, fullname):
        """ Run the cloned repo through pylint, and comment on the PR with
        the results """
        [repo_owner, repo_name] = self.repo['full_name'].split('/')
        path = os.path.join(self.__path, self.config['module'])
        gihu = Github(self.config['auth']['username'],
                      self.config['auth']['password'])
        gihu.get_user(
            repo_owner).get_repo(
                repo_name).get_issue(
                    number).create_comment(
                        '**pylint results:**\n\n```\n{0}\n```'.format(
                            lint_to_text(path)))
        shutil.rmtree(path, ignore_errors=True)
