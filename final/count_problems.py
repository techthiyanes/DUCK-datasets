# counts the number of questions contained in the jsonl files in the data directory.
# The output is written to number_of_questions.txt.

import argparse
import os
import json
from collections import defaultdict
from difflib import SequenceMatcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/', help='Path to directory containing subdirectories with jsonl files')
    args = parser.parse_args()

    def common_substring(s1, s2):
        seq_match = SequenceMatcher(None, s1, s2)
        match = seq_match.find_longest_match(0, len(s1), 0, len(s2))
        if match.size < 4:
            return None
        return s1[match.a:match.a + match.size]

    def count_questions(filepath):
        with open(filepath, 'r') as f:
            count = 0
            for line in f:
                if line.strip():
                    count += 1
        return count

    directories = defaultdict(list)
    for root, _, files in os.walk(args.data):
        for file in files:
            if file.endswith('.jsonl'):
                filepath = os.path.join(root, file)
                common_subdir = None
                for subdir in directories.keys():
                    common_str = common_substring(os.path.basename(root), subdir)
                    if common_str:
                        common_subdir = subdir
                        break

                if common_subdir:
                    directories[common_subdir].append(filepath)
                else:
                    directories[os.path.basename(root)].append(filepath)

    with open('output.txt', 'w') as output_file:
        output_file.write(f'Number of Questions:\n\n')
        for subdir, filepaths in directories.items():
            output_file.write(f'{os.path.join(args.data, subdir)}\n')
            for filepath in filepaths:
                question_count = count_questions(filepath)
                output_file.write(f'\t{filepath}: {question_count} questions\n')
            output_file.write('\n')

if __name__ == '__main__':
    main()
