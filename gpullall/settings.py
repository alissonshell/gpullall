import os
import sys
import signal


def handler_signal(signum, frame):
    from gpullall.colors import Colors

    print(Colors.YELLOW
          + '\nLeaving the application... \nBye'
          + Colors.NC)
    sys.exit(0)


def check_args(args):
    from gpullall import syshelpers

    global fullscan
    global path
    global confirmpull
    global ignore
    global commit
    global stash
    global addchanges
    if args.directory:
        path = str(args.directory[0])
    else:
        if args.fullscan:
            fullscan = True
            path = os.path.abspath(os.sep)
        else:
            path = syshelpers.read_path()

    if args.confirmall:
        confirmpull = True

    if args.ignore:
        ignore = str(args.ignore[0]).split(',')

    if args.add:
        addchanges = True

    if args.commit:
        commit = True

    if args.stash:
        stash = True


def init():
    from gpullall import githelpers
    from gpullall.argparser import parser

    global fullscan
    global path
    global confirmpull
    global path_exists
    global dir_exists
    global ignore
    global addchanges
    global commit
    global stash
    fullscan = False
    path = ""
    confirmpull = False
    path_exists = False
    dir_exists = False
    ignore = []
    addchanges = False
    commit = False
    stash = False

    signal.signal(signal.SIGINT, handler_signal)

    check_args(parser.parse_args())

    repositories = githelpers.get_repositories(path, ignore)
    for counter, repo in enumerate(repositories):
        githelpers.repo_actions(counter, repo, len(repositories))
