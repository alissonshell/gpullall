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
    global ignore
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


def init():
    global fullscan
    global path
    global confirmpull
    global path_exists
    global dir_exists
    global ignore
    fullscan = False
    path = ""
    confirmpull = False
    path_exists = False
    dir_exists = False
    ignore = []

    signal.signal(signal.SIGINT, handler_signal)

    check_args(parser.parse_args())

    repositories = githelpers.get_repositories(path, ignore)
    for counter, repo in enumerate(repositories):
        githelpers.repo_actions(counter, repo, len(repositories))
