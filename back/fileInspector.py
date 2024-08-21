from .folder import Folder
from .file import File
import os
from time import ctime, strptime
from fs.osfs import OSFS
from fs import open_fs


class FileInspector:
    def __init__(self, dir):
        if self._check_dir(dir):   
            self.dir = dir
        else: 
            raise ValueError('Нет такой папки')

    def _check_dir(self, dir) -> bool:
       return os.path.exists(dir)
        # Функция для проверки на существование папки

    # def get_files(self):
    #     files = []
    #     for filename in os.listdir(self.dir):
    #         f = os.path.join(self.dir, filename)
    #         if os.path.isfile(f):
    #             ct = ctime(os.path.getctime(f))
    #             t = strptime(ct)
    #             s = os.path.getsize(f)
    #             files.append(File(f, s, t))
    #         else:
    #             ct = ctime(os.path.getctime(f))
    #             t = strptime(ct)
    #             s = os.path.getsize(f)
    #             files.append(Folder(f, s, t))       
    #     return files
       
    
    def get_sorted_files(self, reverse = False):
        return sorted(self.get_files(), key=lambda f:f.size, reverse=reverse)
    

if __name__ == "__main__":
    inspector = FileInspector("C:/Users/Gleb77/Downloads")
    print(len(inspector.get_sorted_files(True)))
    for f in inspector.get_sorted_files(True):
        print(f)