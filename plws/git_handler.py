from git import Repo, Git
import os
import tempfile

class GitHandler(object):
    def __init__(self, clone_url, branch, commit):
        self.__clone_url = clone_url
        self.__branch = branch
        self.__commit = commit
        self.__path = None

    def clone(self):
        self.__path = self.__getTempFolder()

        Repo.clone_from(self.__clone_url, self.__path)

        git = Git(self.__path)

        git.checkout(self.__branch)

        repo = Repo(self.getPath())
        repo.commit(self.__commit)

    def __getTempFolder(self):
        tmp = os.path.join(tempfile.gettempdir(), str(os.times()[-1]))
        os.makedirs(tmp)

        return tmp

    def getPath(self): return self.__path
