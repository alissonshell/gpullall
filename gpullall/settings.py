import os
import sys
import signal
import syshelpers
import githelpers
from colors import colors
from argparser import parser


def handler_signal(signum, frame):
    print(colors.YELLOW
          + '\nLeaving the application... \nBye'
          + colors.NC)
    sys.exit(0)


def check_args(args):
    global fullscan
    global path
    global confirmpull
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


def init():
    global fullscan
    global path
    global confirmpull
    global path_exists
    global dir_exists
    fullscan = False
    path = ""
    confirmpull = False
    path_exists = False
    dir_exists = False

    signal.signal(signal.SIGINT, handler_signal)

    check_args(parser.parse_args())

    repositories = githelpers.get_repositories(path)
    for counter, repo in enumerate(repositories):
        githelpers.repo_actions(counter, repo, len(repositories))
