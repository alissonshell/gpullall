import os
import git
import settings
import exceptions
import progressbar
from colors import colors


def get_repositories(path, ignore):
    result = []

    for root, dirnames, _ in os.walk(str(path)):
        dirnames[:] = [d for d in dirnames if d not in ignore]
        for dirname in dirnames:
            if dirname == ".git":
                print(colors.GREEN
                      + "GIT repository found: "
                      + os.path.basename(root)
                      + colors.NC)
                result.append(os.path.abspath(root))
    return result


def pull_repo(repo):
    try:
        gitRepository = git.Repo(repo)
        origin = gitRepository.remotes.origin
        pb = progressbar.ProgressBar()
        pb.setup(os.path.basename(repo))
        pullresult = origin.pull(progress=pb)[0]
        print("\n")
        if pullresult.flags == 64:
            print(colors.GREEN
                  + "Repository updated."
                  + colors.NC)
        elif pullresult.flags == 4:
            print(colors.GREEN
                  + "Already up to date."
                  + colors.NC)
        elif pullresult.flags == 16:
            exceptions.pull_rejected()
        print("\n")
    except git.GitCommandError as ex:
        exceptions.show_err(ex)


def repo_actions(counter, repo, rep):

    print(colors.YELLOW
          + "Repository: "
          + repo
          + colors.NC)
    branch = git.Repo(repo).active_branch.name
    print(colors.CYAN
          + "Current branch: "
          + branch
          + colors.NC)
    if settings.confirmpull:
        pull_repo(repo)
    else:
        option = input("Do you want to pull "
                       + os.path.basename(repo)
                       + "from remote? Y/n ")
        if option == "Y":
            pull_repo(repo)
        else:
            exceptions.repo_not_updated(repo)
    if counter not in {1, rep - 1}:
        print(colors.PURPLE
              + "========    "
              + colors.CYAN
              + "Next Repo    "
              + colors.PURPLE
              + "========"
              + colors.NC)
    else:
        print(colors.YELLOW
              + "End."
              + colors.NC)
