import os
from colors import colors


def show_err(ex):
    if ex.stdout:
        print("\n"
              + colors.RED
              + "ERROR: "
              + ex.stdout.replace('stdout: ', '').replace('\'', '"')
              + colors.NC)
    if ex.stderr:
        print("\n"
              + colors.RED
              + "ERROR: "
              + ex.stderr.replace('stderr: ', '').replace('\'', '"')
              + colors.NC)
    print(colors.YELLOW
          + "Command \""
          + ex._cmdline
          + "\" couldn't be done"
          + colors.NC)


def folder_not_found(path):
    print(colors.RED
          + "The folder "
          + str(path)
          + " has not been found."
          + colors.NC)


def pull_rejected():
    print(colors.RED
          + "Pull rejected."
          + colors.NC)


def repo_not_updated(repo):
    print(colors.RED
          + "The repository "
          + os.path.basename(repo)
          + " will not be updated."
          + colors.NC)
