import os
import git


def get_repositories(path, ignore):
    from gpullall.colors import Colors

    result = []

    for root, directories, _ in os.walk(str(path)):
        directories[:] = [d for d in directories if d not in ignore]
        for directory in directories:
            if directory == ".git":
                print(Colors.GREEN
                      + "GIT repository found: "
                      + os.path.basename(root)
                      + Colors.NC)
                result.append(os.path.abspath(root))
    return result


def commit_repo(repo):
    from gpullall import exceptions
    try:
        gitrepository = git.Repo(repo)
        index = gitrepository.index
        print(Colors.YELLOW
              + "Commiting changes on repository."
              + Colors.NC)
        index.commit('Merging conflicts while pulling repository.')
        print(Colors.GREEN
              + "The changes have been committed."
              + Colors.NC)
    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def pull_repo(repo):
    from gpullall import progressbar
    from gpullall.colors import Colors
    from gpullall import exceptions
    from gpullall import settings

    try:
        gitrepository = git.Repo(repo)
        if gitrepository.is_dirty():
            print(Colors.YELLOW
                  + "There are pending changes in the repository."
                  + Colors.NC)
            if settings.commit:
                commit_repo(repo)
            elif not settings.commit and not settings.stash:
                option = input("Do you want to commit your changes? "
                               + "Y/n: ")
                if option == "Y":
                    settings.commit = True
                    commit_repo(repo)
            if settings.stash:
                git_stash(repo)
            elif not settings.commit and not settings.stash:
                option = input("Do you want to stash your changes? "
                               + "Y/n: ")
                if option == "Y":
                    settings.stash = True
                    git_stash(repo)
        origin = gitrepository.remotes.origin
        pb = progressbar.ProgressBar()
        pb.setup(os.path.basename(repo))
        pullresult = origin.pull(progress=pb)[0]
        pb.finish()
        print("\n")
        if pullresult.flags == 64:
            print(Colors.GREEN
                  + "Repository updated."
                  + Colors.NC)
        elif pullresult.flags == 4:
            print(Colors.GREEN
                  + "Already up to date."
                  + Colors.NC)
        elif pullresult.flags == 16:
            exceptions.pull_rejected()
        if settings.stash:
            git_stash_apply(repo)
        print("\n")
    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def repo_actions(counter, repo, rep):
    from gpullall.colors import Colors
    from gpullall import settings
    from gpullall import exceptions

    print(Colors.YELLOW
          + "Repository: "
          + repo
          + Colors.NC)
    branch = git.Repo(repo).active_branch.name
    print(Colors.CYAN
          + "Current branch: "
          + branch
          + Colors.NC)
    if settings.confirmpull:
        pull_repo(repo)
    else:
        option = input("Do you want to pull "
                       + os.path.basename(repo)
                       + " from remote? Y/n ")
        if option == "Y":
            pull_repo(repo)
        else:
            exceptions.repo_not_updated(repo)
    if counter not in {1, rep - 1}:
        print(Colors.PURPLE
              + "========    "
              + Colors.CYAN
              + "Next Repo    "
              + Colors.PURPLE
              + "========"
              + Colors.NC)
    else:
        print(Colors.YELLOW
              + "End."
              + Colors.NC)


def git_stash(repo):
    from gpullall import exceptions
    try:
        gitrepository = git.Repo(repo)
        gitrepository.git.stash('save')
        print(Colors.YELLOW
              + "Your changes have been stashed."
              + Colors.NC)
    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def git_stash_apply(repo):
    from gpullall import exceptions
    try:
        gitrepository = git.Repo(repo)
        gitrepository.git.stash('apply')
        print(Colors.GREEN
              + "Your stashed changes have been applied."
              + Colors.NC)
        print(Colors.YELLOW
              + "Dropping the stash..."
              + Colors.NC)
        gitrepository.git.stash('drop')
    except git.GitCommandError as ex:
        exceptions.show_err(ex)
