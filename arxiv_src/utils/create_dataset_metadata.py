import os
import json
import glob
from tqdm import tqdm

ROOT_DIR = ""  # directory where arxiv_pairs is located

SPLIT_FRAC = {
    "train": 0.9,
    "validation": 0.1,
}

assert os.path.exists(os.path.join(ROOT_DIR, "arxiv_pairs"))

if os.path.exists(os.path.join(ROOT_DIR, "dataset")):
    os.system("rm -rf {}".format(os.path.join(ROOT_DIR, "dataset")))

split_start = {}
split_end = {}
acc_size = 0
for split in SPLIT_FRAC:
    os.makedirs(os.path.join(ROOT_DIR, "dataset", split))
    split_start[split] = acc_size
    split_end[split] = int(acc_size + SPLIT_FRAC[split] * len(os.listdir(os.path.join(ROOT_DIR, "arxiv_pairs"))))
    acc_size = split_end[split]

for i, arxiv_id in enumerate(tqdm(os.listdir(os.path.join(ROOT_DIR, "arxiv_pairs")))):
    arxiv_path = os.path.join(ROOT_DIR, "arxiv_pairs", arxiv_id)
    if not os.path.isdir(arxiv_path) or not os.path.exists(os.path.join(arxiv_path, "tex")) or not os.path.exists(os.path.join(arxiv_path, "png")):
        continue
    tex_files = glob.glob(os.path.join(arxiv_path, "tex", "*.tex"))
    png_files = glob.glob(os.path.join(arxiv_path, "png", "*.png"))

    if len(tex_files) != len(png_files):
        continue

    for png_file in png_files:
        png_file_name = os.path.basename(png_file)
        tex_file_name = "out" + png_file_name.split("-")[1].split(".")[0].lstrip("0") + ".tex"
        tex_file = os.path.join(arxiv_path, "tex", tex_file_name)
        assert os.path.exists(tex_file)

        with open(tex_file, "r") as f:
            tex_contents = f.read()

        if not tex_contents.strip():  # skip empty text
            continue
        
        new_file_name = "_".join([arxiv_id, png_file_name])
        line = json.dumps({
            "file_name": new_file_name,
            "ground_truth": json.dumps({
                "gt_parse": {
                    "text_sequence": tex_contents
                },
                "gt_parse_file": os.path.join("arxiv_pairs", arxiv_id, "tex", tex_file_name)
            })
        }) + "\n"

        for split in SPLIT_FRAC:
            if split_start[split] <= i < split_end[split]:
                original_path = os.path.join("arxiv_pairs", arxiv_id, "png", png_file_name)
                new_path = os.path.join("dataset", split, new_file_name)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.symlink(os.path.relpath(original_path, os.path.dirname(new_path)), new_path)
                with open(os.path.join(ROOT_DIR, "dataset", split, "metadata.jsonl"), "a") as f:
                    f.write(line)
