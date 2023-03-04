import argparse
import os
import shutil

# Remove all folders/files from dir besides tex and png
for f in os.listdir():
    if f != "tex" and f != "png":
        if os.path.isdir(f):
            shutil.rmtree(f)
        else:
            os.remove(f)

# Remove empty tex, png pairs
for f in os.listdir("tex"):
    num = f.split(".tex")[0].split("out-")[0]
    with open(os.path.join("tex", f), "r") as f:
        lines = f.readlines()
        if len(lines) < 2:
            os.remove(os.path.join("tex", f))
            os.remove(os.path.join("png", "out-{}.png".format(num)))

