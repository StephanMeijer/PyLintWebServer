from pylint import lint
from pylint.reporters.text import TextReporter

class WritableObject(object):
    def __init__(self):
        self.content = []
    def write(self, st):
        self.content.append(st)
    def read(self):
        return self.content

def lint_to_text(paths):
    pylint_output = WritableObject()
    for path in paths:
        lint.Run(path, reporter=TextReporter(pylint_output), exit=False)
    return "".join(pylint_output.read())
