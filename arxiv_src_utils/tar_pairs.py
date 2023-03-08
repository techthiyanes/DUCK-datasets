import tarfile
import argparse
import os
import glob
import multiprocessing as mp
from tqdm import tqdm
from pathlib import Path


def untar_download(arxiv_src, output_dir, tar_batch):
    for tar_file in tar_batch:
        file_path = os.path.join(arxiv_src, tar_file)
        with tarfile.open(file_path, "r") as tf:
            tf.extractall(path=output_dir)


def run_untar(arxiv_src, output_dir, num_workers):
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


def tar_dirs(output_dir, dir_batch, cnt):
    for tex_dirs in tqdm(dir_batch):
        tar_name = os.path.join(output_dir, "arxiv_pairs_{}.tar".format(cnt))
        cnt += 1
        # Recommended not to compress for data transfer
        tar = tarfile.open(tar_name, "w:")
        for tex_dir in tex_dirs:
            tar.add(tex_dir)
        tar.close()


def run_tar(input_dir, output_dir, tar_batch_size, num_workers):
    os.chdir(input_dir)
    dirs = glob.glob("*")
    batch_size = len(dirs) // num_workers
    num_workers = (len(dirs) + batch_size - 1) // batch_size
    dir_batches = [dirs[batch_size * i : batch_size * (i+1)] for i in range(num_workers)]
    ps = []
    cnt = 0
    for dir_batch in dir_batches:
        num_tar_batches = (len(dir_batch) + tar_batch_size - 1) // tar_batch_size
        dir_batch = [dir_batch[i * tar_batch_size : (i+1) * tar_batch_size] for i in range(num_tar_batches)] 
        p = mp.Process(target=tar_dirs, args=[output_dir, dir_batch, cnt])
        cnt += num_tar_batches
        ps.append(p)
        p.start()

    for p in ps:
        p.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--num_workers", type=int)
    parser.add_argument("--tar_batch_size", default=128, type=int)
    parser.add_argument("--untar", action="store_true")

    args = parser.parse_args()

    print("Number of cpu available: ", mp.cpu_count())
    print("Using {} cpu".format(args.num_workers))

    # Make output dir
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    if args.untar:
        run_untar(args.input_dir, args.output_dir, args.num_workers)
    else:
        run_tar(args.input_dir, args.output_dir, args.tar_batch_size, args.num_workers)
