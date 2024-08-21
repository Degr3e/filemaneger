from fs.osfs import OSFS
from fs import open_fs


home_fs = OSFS("~/") 
print(home_fs.listdir("/"))
my_fs = open_fs("c:/")
my_fs.tree()