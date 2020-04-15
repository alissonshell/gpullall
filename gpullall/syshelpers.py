import os


def remove_file(file):
    os.remove(file)


def read_path():
    from gpullall import settings
    from gpullall import exceptions

    print("Let's find the directory you want to scan.")

    while not settings.dir_exists:
        settings.path = input("Enter the path: ")
        if os.path.exists(settings.path):
            settings.dir_exists = True
        else:
            exceptions.folder_not_found(settings.path)
    return settings.path
