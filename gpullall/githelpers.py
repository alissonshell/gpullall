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
    from gpullall.colors import Colors
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

    dostash = False
    gitmail = ""

    try:
        gitrepository = git.Repo(repo)
        if gitrepository.is_dirty():
            print(Colors.YELLOW
                  + "There are pending changes in the repository."
                  + Colors.NC)
            print("\n")
            print(Colors.RED
                  + "Your local chagens could be overwritten."
                  + Colors.NC)
            print("\n")

            if settings.addchanges:
                gitrepository.git.add(u=True)
            elif not settings.addchanges:

                option = input("Do you want to add all your local changes "
                               + "to Git's \"Staging Area\"? "
                               + "Y/n: ")
                if option == "Y":
                    gitrepository.git.add(u=True)

            gitmail = gitrepository.config_reader().get_value("user", "email")
            if not gitmail:
                gitmail = temporary_user_config(repo)

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
                    dostash = True
                    git_stash(repo)
        origin = gitrepository.remotes.origin
        previousflag = origin.fetch()[0]
        pb = progressbar.ProgressBar()
        pb.setup(os.path.basename(repo))
        origin.pull(progress=pb)
        pb.finish()
        print("\n")
        if previousflag.flags == 64:
            print(Colors.GREEN
                  + "Repository updated."
                  + Colors.NC)
        elif previousflag.flags == 4:
            print(Colors.GREEN
                  + "Already up to date."
                  + Colors.NC)
        elif previousflag.flags == 16:
            exceptions.pull_rejected()
        if dostash:
            git_stash_apply(repo)
        print("\n")
        if gitmail == "gpullall@gpullallmail.ex":
            remove_temporary_user_config(repo)

    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def repo_actions(counter, repo, rep):
    from gpullall.colors import Colors
    from gpullall import settings
    from gpullall import exceptions

    try:
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
    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def git_stash(repo):
    from gpullall import exceptions
    from gpullall.colors import Colors

    try:
        gitrepository = git.Repo(repo)
        gitrepository.git.stash('--keep-index')
        print(Colors.YELLOW
              + "Your changes have been stashed."
              + Colors.NC)
    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def git_stash_apply(repo):
    from gpullall import exceptions
    from gpullall.colors import Colors

    try:
        gitrepository = git.Repo(repo)
        gitrepository.git.stash('apply')
        print(Colors.GREEN
              + "Your stashed changes have been applied."
              + Colors.NC)
        print("\n")
        print(Colors.YELLOW
              + "Dropping the stash..."
              + Colors.NC)
        gitrepository.git.stash('drop')
    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def temporary_user_config(repo):
    from gpullall.colors import Colors

    gitrepository = git.Repo(repo)

    print(Colors.YELLOW
          + "There's no global user"
          + "configuration for this repository."
          + Colors.NC)
    gitrepository.config_writer().set_value("user",
                                            "name",
                                            "gpullall").release()
    clean_config_lock(repo)
    gitrepository.config_writer().set_value("user",
                                            "email",
                                            "gpullall@gpullallmail.ex")
    clean_config_lock(repo)
    print("\n")
    print(Colors.PURPLE
          + "user gpullall"
          + " and email gpullall@gpullallmail.ex"
          + " have been created to stash/commit the repository."
          + Colors.NC)
    print("\n")
    return "gpullall@gpullallmail.ex"


def remove_temporary_user_config(repo):
    gitrepository = git.Repo(repo)

    clean_config_lock(repo)
    gitrepository.config_writer().set_value("user",
                                            "name",
                                            "").release()
    clean_config_lock(repo)
    gitrepository.config_writer().set_value("user",
                                            "email",
                                            "")
    clean_config_lock(repo)


def clean_config_lock(repo):
    from gpullall import syshelpers

    gitrepository = git.Repo(repo)

    configlockfile = gitrepository.working_tree_dir + "/.git/config.lock"

    if os.path.isfile(configlockfile):
        syshelpers.remove_file(configlockfile)
