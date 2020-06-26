import argparse
from gpullall.colors import Colors

parser = argparse.ArgumentParser(description='Pull all your GIT repositories.')
parser.add_argument('--directory',
                    '-D',
                    help="Enter a directory manually.",
                    nargs=1)
parser.add_argument('--confirmall',
                    '-Y',
                    help="Confirm to pull every single"
                         + "repository found automatically.",
                    action="store_true")
parser.add_argument('--fullscan',
                    '-F',
                    help="Search git repositories in the disk.",
                    action="store_true")
parser.add_argument('--ignore',
                    '-I',
                    help="Ignore repositories. eg: "
                         + "--ignore repo1,repo2,repo3...",
                    nargs=1)
parser.add_argument('--add',
                    '-A',
                    help="Add local changes to Git's \"Staging Area\"",
                    action="store_true")
mergeoptions = parser.add_mutually_exclusive_group(required=False)
mergeoptions.add_argument('--commit',
                          '-C',
                          help="Commites changes on your repositories. "
                               + Colors.RED
                               + "(May not be used with --stash)"
                               + Colors.NC,
                               action="store_true")
mergeoptions.add_argument('--stash',
                          '-S',
                          help="Stashes changes on your "
                               + "repositories before pull. "
                               + Colors.RED
                               + "(May not be used with --commit)"
                               + Colors.NC,
                               action="store_true")
