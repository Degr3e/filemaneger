import eel
from gen.middle.mid_app import *

# import os
# from time import ctime, strptime
 
# directory = 'C:/Users/Gleb77/Downloads'
# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     if os.path.isfile(f):
#         ct = ctime(os.path.getctime(f))
#         print(strptime(ct))


if __name__ == "__main__":
    eel.init("gen/front")
    eel.start("index.html", mode="chrome", size=(760, 760), )