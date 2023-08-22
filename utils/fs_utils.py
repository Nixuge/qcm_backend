import os


def mkdir_if_not_exist(loc: str):
    if not os.path.isdir(loc):
        os.makedirs(loc)