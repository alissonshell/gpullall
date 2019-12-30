import os


def show_err(ex):
    from gpullall.colors import Colors

    if ex.stdout:
        print("\n"
              + Colors.RED
              + "ERROR: "
              + ex.stdout.replace('stdout: ', '').replace('\'', '"')
              + Colors.NC)
    if ex.stderr:
        print("\n"
              + Colors.RED
              + "ERROR: "
              + ex.stderr.replace('stderr: ', '').replace('\'', '"')
              + Colors.NC)
    print(Colors.YELLOW
          + "Command \""
          + ex.stderr
          + "\" couldn't be done"
          + Colors.NC)


def folder_not_found(path):
    from gpullall.colors import Colors

    print(Colors.RED
          + "The folder "
          + str(path)
          + " has not been found."
          + Colors.NC)


def pull_rejected():
    from gpullall.colors import Colors

    print(Colors.RED
          + "Pull rejected."
          + Colors.NC)


def repo_not_updated(repo):
    from gpullall.colors import Colors

    print(Colors.RED
          + "The repository "
          + os.path.basename(repo)
          + " will not be updated."
          + Colors.NC)
