import os
import subprocess
from tqdm import tqdm
from threading import Thread, Semaphore

sem = Semaphore(4)

def run(sem, file_dir):
    try:
        subprocess.run(["./tex2png.sh", file_dir, "3&>/dev/null"], capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    finally:
        sem.release()

Ts = []
for file_dir in tqdm(os.listdir()):
    if ".tex" in file_dir:
        # Check if \end{document} at end of file. If not add it
        with open(file_dir, "r+") as f:
            lines = f.readlines()
            if "\end{document}" not in lines[-1]:
                f.write("\n\\end{document}")
        file_dir = file_dir.split(".tex")[0]
        sem.acquire()
        T = Thread(target=run, args=(sem, file_dir))
        T.start()
        Ts.append(T)

for T in Ts:
    T.join()
