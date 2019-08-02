import argparse

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
                    help="Ignore a folder(s). eg: --ignore dir1,dir2,dir3...",
                    nargs=1)
