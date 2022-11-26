import os
import subprocess
from tqdm import tqdm
import shutil
import multiprocessing as mp


def run(file_dir, verbose=True):
    if verbose:
        print(file_dir)
    subprocess.run(["./tex2png.sh", file_dir, "3&>/dev/null"], capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def dispatch(file_dir):
    try:
        result = pool.apply_async(run, [file_dir])
        result.get(10)
    except mp.context.TimeoutError:
        print("TIMEOUT")
        if os.path.isdir(file_dir):
            shutil.rmtree(file_dir)

pool = mp.Pool(2)
for file_dir in tqdm(os.listdir()):
    if ".tex" in file_dir:
        # Check if \end{document} at end of file. If not add it
        with open(file_dir, "r+") as f:
            lines = f.readlines()
            if "\end{document}" not in lines[-1]:
                f.write("\n\\end{document}")
        file_dir = file_dir.split(".tex")[0]
        dispatch(file_dir)
