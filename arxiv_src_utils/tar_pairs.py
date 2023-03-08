import tarfile
import argparse
import os
import glob
import multiprocessing as mp
from tqdm import tqdm


def tar_dirs(output_dir, dir_batch, cnt):
    for tex_dirs in tqdm(dir_batch):
        tar_name = os.path.join(output_dir, "arxiv_pairs_{}.tar".format(cnt))
        cnt += 1
        # Recommended not to compress for data transfer
        tar = tarfile.open(tar_name, "w:")
        for tex_dir in tex_dirs:
            tar.add(tex_dir)
        tar.close()

def run(input_dir, output_dir, tar_batch_size, num_workers):
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

    args = parser.parse_args()

    print("Number of cpu available: ", mp.cpu_count())
    print("Using {} cpu".format(args.num_workers))

    run(args.input_dir, args.output_dir, args.tar_batch_size, args.num_workers)
