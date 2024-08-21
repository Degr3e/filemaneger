import eel, json
from fs import open_fs
from fs.opener.errors import UnsupportedProtocol
from fs.errors import CreateFailed
import os, sys


@eel.expose    
def get_files(directory):
    fs = open_fs(directory)
    try:
        files = json.dumps([fs.getinfo(f.name, namespaces=['details', 'basic']).raw for f in list(fs.scandir("/"))])
    except (UnsupportedProtocol, CreateFailed) as e:
        return False
    except e:
        print("Произошла ошибка доступа")
        print(e)
        return False
    return files

# def get_all_files(path):
#     files = open_fs(path)

def get_all_files(directory):
    fs = open_fs(directory)
    tree = {directory : []}
    for path in list(fs.scandir("/")):
        if path.is_file:
            tree[directory].append(path)
        else:
            # print(path.make_path(directory))
            tree[directory].append(get_all_files(path.make_path(directory) + "/"))
    return tree
def get_all_files_from_home(directory):
    fs = open_fs(directory)
    tree = {directory : []}
    for path in fs.walk.files(filter=['*.py']):
        print(path)
if __name__ == "__main__":
    print(get_all_files_from_home("D:/"))