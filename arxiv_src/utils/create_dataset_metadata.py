# This script creates a metadata.jsonl file.
# To create train/val/test splits, use head and tail commands, e.g.:
# head -n 800 metadata.jsonl > train.jsonl
# tail -n 80  metadata.jsonl > val.jsonl

import os
import json
import glob
from tqdm import tqdm

ROOT_DIR = ""  # directory where arxiv_pairs is located

assert os.path.exists(os.path.join(ROOT_DIR, "arxiv_pairs"))

if os.path.exists(os.path.join(ROOT_DIR, "metadata.jsonl")):
    os.remove(os.path.join(ROOT_DIR, "metadata.jsonl"))

for arxiv_id in tqdm(os.listdir(os.path.join(ROOT_DIR, "arxiv_pairs"))):
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
        
        line = json.dumps({
            "file_name": os.path.join("arxiv_pairs", arxiv_id, "png", png_file_name),
            "ground_truth": json.dumps({
                "gt_parse": {
                    "text_sequence": tex_contents
                },
                "gt_parse_file": os.path.join("arxiv_pairs", arxiv_id, "tex", tex_file_name)
            })
        })
        with open(os.path.join(ROOT_DIR, "metadata.jsonl"), "a") as f:
            f.write(line + "\n")
