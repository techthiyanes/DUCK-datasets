import os
import subprocess
from tqdm import tqdm
import shutil
import multiprocessing as mp


def run(file_dir, verbose=True):
    if verbose:
        print(file_dir)
    subprocess.run(["./tex2png.sh", file_dir, "3&>/dev/null"], capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


batch_size = 4
TIMEOUT = 15
pool = mp.Pool(batch_size)
pool2 = mp.Pool(batch_size)
tex_files = os.listdir()
tex_files = list(filter(lambda x: ".tex" in x, tex_files))
num_batches = (len(tex_files) + batch_size - 1) // batch_size
tex_batches = [tex_files[batch_size*i : batch_size*(i+1)] for i in range(num_batches)]

for batch in tqdm(tex_batches):
    # Check if \end{document} at end of file. If not add it
    ps = []
    for file_dir in batch:
        with open(file_dir, "r+") as f:
            lines = f.readlines()
            if "\end{document}" not in lines[-1]:
                f.write("\n\\end{document}")
        file_dir = file_dir.split(".tex")[0]
        p = mp.Process(target=run, args=[file_dir])
        ps.append(p)
        p.start()

    for i, p in enumerate(ps):
        if i == 0:
            p.join(TIMEOUT)
        else:
            p.join(0)
        if p.is_alive():
            print("TIMEOUT")
            p.terminate()
            p.join()
            if os.path.isdir(file_dir):
                shutil.rmtree(file_dir)     
