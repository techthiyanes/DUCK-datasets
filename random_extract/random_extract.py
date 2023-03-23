import argparse
import json
import random
from typing import List

def extract_entries(input_files: List[str], n:int, ratios: List[float]) -> List[dict]:
    entries = []
    for file_path, ratio in zip(input_files, ratios):
        with open(file_path, 'r') as file:
            file_entries = [json.loads(line) for line in file]
            length = min(len(file_entries),n*ratio)
            num_entries = int(length)
            entries.extend(random.sample(file_entries, num_entries))
    return entries

def main(input_files: List[str], n: int, ratios: List[float]):
    if not ratios:
        ratios = [1 / len(input_files)] * len(input_files)

    if len(input_files) != len(ratios) or abs(sum(ratios) - 1) > 1e-6:
        raise ValueError("Ratios length must be equal to input files length and sum to 1")

    entries = extract_entries(input_files, n, ratios)
    random.shuffle(entries)
    selected_entries = entries[:n]

    with open('output.jsonl', 'w') as output_file:
        for entry in selected_entries:
            output_file.write(json.dumps(entry) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new JSONL file with random entries from input files")
    parser.add_argument("input_files", nargs='+', help="List of file paths")
    parser.add_argument("n", type=int, help="Length of the output JSONL file")
    parser.add_argument("--ratios", nargs='*', type=float, default=[], help="List of ratios, summing up to 1")

    args = parser.parse_args()
    main(args.input_files, args.n, args.ratios)
