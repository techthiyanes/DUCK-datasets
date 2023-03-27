# code for generating test/val splits for mcat problems 
# the code: 
# 1. reads in the mcat file
# 2. groups together problems with the same problem passage
# 3. splits the mcat file into train/val/test splits
# 4. writes the train/val/test splits to jsonl files


import jsonlines
import os
import argparse
from typing import Dict, List, Set
import random

def validate_file(file_path: str, extension: str) -> None:
    if not os.path.exists(file_path):
        raise ValueError(f"The file path '{file_path}' does not exist.")
    if not file_path.endswith(extension):
        raise ValueError(f"The file '{file_path}' is not of the correct file type '{extension}'.")

def same_passage(problem1: Dict, problem2: Dict, N: int) -> bool:
    return problem1["Problem Statement"][:N] == problem2["Problem Statement"][:N]

def problems_wwo_images(files: str, images: bool = False):
    # generate a list of problems with/without images
    # depending on the value of `images` flag
    problems = []
    with jsonlines.open(files, mode='r') as reader:
        for problem in reader:
            if images and problem["Images"]:
                problems.append(problem)
            elif not images and not problem["Images"]:
                problems.append(problem)
    return problems


def create_shared_passage_sets(problem_list: List[str], N: int) -> List[Set[Dict]]:
    shared_passages = []
    for problem in problem_list:
        found_shared = False
        for passage_set in shared_passages:
            if any(same_passage(problem, other_problem, N) for other_problem in passage_set):
                passage_set.append(problem)
                found_shared = True
                break
        if not found_shared:
            shared_passages.append([problem])
    return shared_passages

def valsize(sorted_shared_passages: List[Set[Dict]], splits: Dict[str,int], images: bool = False): 
    # size of the validation set 
    # return closest integer value that exceeds the desired size
    total_size = sum(len(passage_set) for passage_set in sorted_shared_passages)
    desired_size = int(total_size * splits["valid"])
    # take smallest sum of passage set sizes that exceeds the desired size
    output = 0
    for passage_set in sorted_shared_passages:
        output += len(passage_set)
        if output >= desired_size:
            break
    return output


def write_splits_to_files(val_file: str, test_file: str, sorted_shared_passages: List[Set[Dict]], splits: Dict[str,int], images: bool = False) -> None:
    total_size = sum(len(passage_set) for passage_set in sorted_shared_passages)
    val_size = valsize(sorted_shared_passages, splits, images = images)

    with jsonlines.open(val_file, mode='w') as val_writer, jsonlines.open(test_file, mode='w') as test_writer:
        val_count = 0
        for passage_set in sorted_shared_passages:
            for problem in passage_set:
                if val_count < val_size:
                    val_writer.write(problem)
                    val_count += 1
                else:
                    test_writer.write(problem)


def main(input_file: str, val_file: str, test_file: str, splits: Dict[str,int] = {"valid": 0.5, "test": 0.5}, N: int = 30, images: bool = False):
    validate_file(input_file, '.jsonl')
    validate_file(val_file, '.jsonl')
    validate_file(test_file, '.jsonl')

    if abs(sum(splits.values()) - 1) > 1e-9:
        raise ValueError("The sum of the splits should be equal to 1.")

    problem_list = problems_wwo_images(input_file,images = images)
    shared_passages = create_shared_passage_sets(problem_list, N)
    sorted_shared_passages = sorted(shared_passages, key=lambda x: len(x), reverse=True)

    write_splits_to_files(val_file, test_file, sorted_shared_passages, splits)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split JSONL file into validation and test files.")
    parser.add_argument("--input_file", type=str, help="Path to input JSONL file.")
    parser.add_argument("--val_file", type=str, help="Path to validation JSONL file.")
    parser.add_argument("--test_file", type=str, help="Path to test JSONL file.")
    parser.add_argument("--splits", type=float, nargs=2, default=[0.5, 0.5], metavar=("valid", "test"), help="Validation and test splits. The values should sum to 1. Default is 0.5:0.5.")
    parser.add_argument("--N", type=int, default=30, help="Check the first N characters to check if two problems have the same passages. Default value is 30 characters.")
    parser.add_argument("--images", type=str, default=False, help="Whether output file contains problems with images or not. Default is False.")


    args = parser.parse_args()

    main(args.input_file, args.val_file, args.test_file, {"valid": args.splits[0], "test": args.splits[1]}, args.N, args.images)
