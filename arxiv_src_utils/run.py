import argparse
import os
from pathlib import Path
import tarfile
from tqdm import tqdm
import shutil
import gzip
import subprocess
import multiprocessing as mp
import time
import re


def untar_download(arxiv_src, output_dir, tar_batch):
    for tar_file in tar_batch:
        name = tar_file.split(".tar")[0]
        file_path = os.path.join(arxiv_src, tar_file)
        out_path = os.path.join(output_dir, name)
        with tarfile.open(file_path, "r") as tf:
            tf.extractall(path=out_path)


def run_untarring(arxiv_src, output_dir, num_workers):
    # First need to iterate over .tar src files
    print("Untarring files...")
    tars = list(filter(lambda f: ".tar" in f, os.listdir(arxiv_src)))
    print("{} tar files".format(len(tars)))
    batch_size = len(tars) // num_workers
    num_workers = (len(tars) + batch_size - 1) // batch_size
    worker_batches = [tars[batch_size * i : batch_size * (i+1)] for i in range(num_workers)]
    ps = []
    for tar_batch in tqdm(worker_batches, total=len(worker_batches)):
        p = mp.Process(target=untar_download, args=[arxiv_src, output_dir, tar_batch])
        ps.append(p)
        p.start()

    for p in ps:
        p.join()


def extract_tex(output_dir, arxiv_batch):
    for arxiv_dir in arxiv_batch:
        intermediate = os.path.join(output_dir, arxiv_dir)
        intermediate = os.path.join(intermediate, os.listdir(intermediate)[0])
        arxiv_files = list(filter(lambda f: ".gz" in f, os.listdir(intermediate)))
        for i, tex_file in enumerate(arxiv_files):
            if i % 500 == 0:
                print("Starting {} of {}".format(i, len(arxiv_files)))
            folder_name = tex_file.split(".gz")[0]
            folder_path = os.path.join(output_dir, folder_name)

            try:
                with tarfile.open(os.path.join(intermediate, tex_file), "r:gz") as my_tar:
                    my_tar.extractall(folder_path)
            except tarfile.ReadError:
                with gzip.open(os.path.join(intermediate, tex_file), "rb") as f:
                    content = f.read()
                os.mkdir(folder_path)
                with open(os.path.join(folder_path, "main.tex"), "wb") as f:
                    f.write(content)
            
        # Remove used arxiv_dir
        shutil.rmtree(os.path.join(output_dir, arxiv_dir))
    

def run_extraction(arxiv_src, output_dir, num_workers):
    print("Extracting tex...")
    arxiv_dirs = os.listdir(output_dir)
    batch_size = len(arxiv_dirs) // num_workers
    num_workers = (len(arxiv_dirs) + batch_size - 1) // batch_size
    arxiv_batches = [arxiv_dirs[batch_size * i : batch_size * (i+1)] for i in range(num_workers)]
    ps = []
    for arxiv_batch in arxiv_batches:
        p = mp.Process(target=extract_tex, args=[output_dir, arxiv_batch])
        ps.append(p)
        p.start()

    for p in ps:
        p.join()


def process_tex(tex_folder):
    #subprocess.run(["scripts/tex2png.sh {}".format(tex_folder)], shell=True)
    has_tex = False
    for f in os.listdir(tex_folder):
        has_tex = ".tex" in f
    if has_tex:
        subprocess.run(["tex2png.sh {}".format(tex_folder)], capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)


def run_processing(arxiv_src, output_dir, num_workers):
    print("Processing tex...")
    tex_folders = os.listdir(output_dir)
    print("{} tex folders".format(len(tex_folders)))
    num_batches = (len(tex_folders) + num_workers - 1) // num_workers
    tex_batches = [tex_folders[num_workers * i : num_workers * (i+1)] for i in range(num_batches)]
    for tex_batch in tqdm(tex_batches, total=len(tex_batches)):
        ps = []
        for tex_folder in tex_batch:
            p = mp.Process(target=process_tex, args=[os.path.join(output_dir, tex_folder)])
            ps.append(p)
            p.start()

        TIMEOUT = 15
        start_time = time.time()    

        for p in ps:
            remaining_time = TIMEOUT - (time.time() - start_time)
            p.join(max(1, remaining_time))
            if p.is_alive():
                print("TIMEOUT")
                p.terminate()
                p.join()


def postprocessing(output_dir, pair_folders):
    for i, pair_folder in enumerate(pair_folders):
        if i % 100 == 0:
            print("Processing {} of {}".format(i, len(pair_folders)))
        # Remove if more than two files in directory
        if len(os.listdir(os.path.join(output_dir, pair_folder))) != 2:
            shutil.rmtree(os.path.join(output_dir, pair_folder))
            continue
        # Remove pair_folder if no png folder
        if not os.path.isdir(os.path.join(output_dir, pair_folder, "png")):
            shutil.rmtree(os.path.join(output_dir, pair_folder))
            continue
        # Remove pair_folder if png folder is empty
        if len(os.listdir(os.path.join(output_dir, pair_folder, "png"))) == 0:
            shutil.rmtree(os.path.join(output_dir, pair_folder))
            continue
        # Remove pair_folder if no tex folder
        if not os.path.isdir(os.path.join(output_dir, pair_folder, "tex")):
            shutil.rmtree(os.path.join(output_dir, pair_folder))
            continue
        # Remove pair_folder if tex folder is empty
        if len(os.listdir(os.path.join(output_dir, pair_folder, "tex"))) == 0:
            shutil.rmtree(os.path.join(output_dir, pair_folder))
            continue

        # Format tex to remove label, cite, citet, citep, ref content
        try:
            for tex_file in os.listdir(os.path.join(output_dir, pair_folder, "tex")):
                with open(os.path.join(output_dir, pair_folder, "tex", tex_file), "r") as f:
                    lines = f.readlines()
                new_lines = []
                for line in lines:
                    # Replace cite, ref, label with empty cite to avoid guessing/model collapse
                    new_line = re.sub(r"\\cite{.*?}", r"\\cite{}", line)
                    new_line = re.sub(r"\\label{.*?}", r"\\cite{}", new_line)
                    new_line = re.sub(r"\\ref{.*?}", r"\\cite{}", new_line)
                    new_line = re.sub(r"\\eqref{.*?}", r"\\cite{}", new_line)
                    new_line = re.sub(r"\\citet{.*?}", r"\\cite{}", new_line)
                    new_line = re.sub(r"\\citep{.*?}", r"\\cite{}", new_line)
                    new_line = re.sub(r'\\cite\[(.*?)\]\{.*?\}', r'\\cite{}', new_line)
                    new_line = re.sub(r'\\includegraphics\[.*?\]\{.*?\}', r'\\includegraphics\[\]\{\}', new_line)
                    new_lines.append(new_line)
                with open(os.path.join(output_dir, pair_folder, "tex", tex_file), "w") as f:
                    f.writelines(new_lines)
        except UnicodeDecodeError:
            shutil.rmtree(os.path.join(output_dir, pair_folder))


def run_postprocessing(output_dir, num_workers):
    pair_folders = os.listdir(output_dir)
    print("Doing final checks...")
    batch_size = len(pair_folders) // num_workers
    num_workers = (len(pair_folders) + batch_size - 1) // batch_size
    pair_batches = [pair_folders[batch_size * i : batch_size * (i+1)] for i in range(num_workers)]
    ps = []
    for pair_batch in pair_batches:
        p = mp.Process(target=postprocessing, args=[output_dir, pair_batch])
        ps.append(p)
        p.start()

    for p in ps:
        p.join()

    print("Final success rate: ", len(os.listdir(output_dir)) / len(pair_folders))
    print("Total successful compilations: ", len(os.listdir(output_dir)))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--arxiv_src", default="test/")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--num_workers", type=int, default=1)
    
    args = parser.parse_args()

    print("Number of cpu available: ", mp.cpu_count())
    print("Using {} cpu".format(args.num_workers))

    # Make output dir
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    run_untarring(args.arxiv_src, args.output_dir, args.num_workers)
    run_extraction(args.arxiv_src, args.output_dir, args.num_workers)
    run_processing(args.arxiv_src, args.output_dir, args.num_workers)
    run_postprocessing(args.output_dir, args.num_workers)
