import argparse
import json

# the purpose of this script is to sort the mcat file by problem number
# we do this in order to see which problems share the same problem passage

def read_jsonl_file(input_file):
    with open(input_file, 'r') as f:
        data = [json.loads(line) for line in f]
    return data

def write_jsonl_file(output_file, data):
    with open(output_file, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def sort_data(data):
    return sorted(data, key=lambda x: x['Problem Number'])

def main():
    parser = argparse.ArgumentParser(description="Sort a JSONL file by the 'Problem Number' key")
    parser.add_argument('input_file', type=str, help="Input JSONL file")
    parser.add_argument('output_file', type=str, help="Output JSONL file")

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    data = read_jsonl_file(input_file)
    sorted_data = sort_data(data)
    write_jsonl_file(output_file, sorted_data)

if __name__ == "__main__":
    main()
