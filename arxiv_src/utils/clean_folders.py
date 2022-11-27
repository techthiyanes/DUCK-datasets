import os
import shutils

for dir_path in os.listdir():
    if os.path.isdir(dir_path):
        if len(os.path.listdir(os.path.join(os.getcwd(), dir_path))) > 2:
            shutils.rmtree(dir_path)
    else:
        os.remove(dir_path)


