import eel, json
from fs import open_fs
from fs.opener.errors import UnsupportedProtocol
from fs.errors import CreateFailed
import os, sys, shutil


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

# удаляем файлы и папки

def remove(folder):
    if os.path.isfile(folder):
        os.unlink(folder)
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                return False
        shutil.rmtree(folder)
    return True
if __name__ == "__main__":
    # print(get_all_files_from_home("D:/"))
    remove("C:/Users/Gleb77/Documents/!a")