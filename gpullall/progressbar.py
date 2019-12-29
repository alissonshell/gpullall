import git
from progress.bar import IncrementalBar as Bar


class ProgressBar(git.RemoteProgress):

    def __init__(self):
        super().__init__()
        self.bar = Bar()

    def setup(self, repo_name):
        self.bar = Bar(message='git pull {}'.format(repo_name), suffix='')

    def update(self, op_code, cur_count, max_count=100, message=''):
        max_count = int(max_count or 100)
        if max_count != self.bar.max:
            self.bar.max = max_count
        self.bar.goto(int(cur_count))

    def finish(self):
        self.bar.finish()
