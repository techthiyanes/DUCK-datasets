import os
import subprocess
from tqdm import tqdm

for file_dir in tqdm(os.listdir()):
    if ".tex" in file_dir:
        file_dir = file_dir.split(".tex")[0]
        subprocess.run(["./tex2png.sh", file_dir, "3&>/dev/null"], capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
