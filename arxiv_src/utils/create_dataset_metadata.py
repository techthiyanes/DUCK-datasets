import os
import json
import glob
from tqdm import tqdm

ROOT_DIR = ""  # Directory where arxiv_pairs is located.
DATASET_NAME = "arxiv-pairs-dataset"
SPLIT_FRAC = {
    "train": 0.995,
    "validation": 0.005,
}

assert os.path.exists(os.path.join(ROOT_DIR, "arxiv_pairs"))
arxiv_ids = sorted(os.listdir(os.path.join(ROOT_DIR, "arxiv_pairs")))

if os.path.exists(os.path.join(ROOT_DIR, DATASET_NAME)):
    os.system("rm -rf {}".format(os.path.join(ROOT_DIR, DATASET_NAME)))

split_start = {}
split_end = {}
acc_size = 0
for split in SPLIT_FRAC:
    os.makedirs(os.path.join(ROOT_DIR, DATASET_NAME, split))
    split_start[split] = acc_size
    split_end[split] = int(acc_size + SPLIT_FRAC[split] * len(arxiv_ids))
    acc_size = split_end[split]

for i, arxiv_id in enumerate(tqdm(arxiv_ids)):
    arxiv_path = os.path.join(ROOT_DIR, "arxiv_pairs", arxiv_id)
    if not os.path.isdir(arxiv_path) or not os.path.exists(os.path.join(arxiv_path, "tex")) or not os.path.exists(os.path.join(arxiv_path, "png")):
        continue
    tex_files = glob.glob(os.path.join(arxiv_path, "tex", "*.tex"))
    png_files = glob.glob(os.path.join(arxiv_path, "png", "*.png"))

    if len(tex_files) != len(png_files):
        continue
    
    last_is_empty = False
    for png_file in sorted(png_files):
        png_file_name = os.path.basename(png_file)
        tex_file_name = "out" + png_file_name.split("-")[1].split(".")[0].lstrip("0") + ".tex"
        tex_file = os.path.join(arxiv_path, "tex", tex_file_name)
        assert os.path.exists(tex_file)

        with open(tex_file, "r") as f:
            tex_contents = f.read()

        if not tex_contents.strip():  # Skip empty text.
            last_is_empty = True
            continue
        if last_is_empty:
            # Sometimes it happens that few consecutive pages' labels are empty
            # (but the pages aren't actually empty), and all that text gets
            # assigned to the next page. We skip those pages because the label
            # isn't correct.
            last_is_empty = False
            continue
        last_is_empty = False
        
        new_file_name = "_".join([arxiv_id, png_file_name])
        line = json.dumps({
            "file_name": new_file_name,
            "ground_truth": json.dumps({
                "gt_parse": {
                    "text_sequence": tex_contents
                },
                "png_file": os.path.join("arxiv_pairs", arxiv_id, "png", png_file_name),
                "tex_file": os.path.join("arxiv_pairs", arxiv_id, "tex", tex_file_name)
            })
        }) + "\n"

        for split in SPLIT_FRAC:
            if split_start[split] <= i < split_end[split]:
                original_path = os.path.join("arxiv_pairs", arxiv_id, "png", png_file_name)
                new_path = os.path.join(DATASET_NAME, split, new_file_name)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.symlink(os.path.relpath(original_path, os.path.dirname(new_path)), new_path)
                with open(os.path.join(ROOT_DIR, DATASET_NAME, split, "metadata.jsonl"), "a") as f:
                    f.write(line)
