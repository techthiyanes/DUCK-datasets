import os
import json
from pathlib import Path

def process_files(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        rel_path = os.path.relpath(root, input_dir)
        for file in files:
            if file.endswith('.jsonl'):
                with open(os.path.join(root, file), 'r') as input_file:
                    out_dir = os.path.join(output_dir, rel_path)
                    os.makedirs(out_dir, exist_ok=True)
                    with open(os.path.join(out_dir, file), 'w') as output_file:
                        for line in input_file:
                            json_entry = json.loads(line)
                            json_entry = add_problem_type(file, json_entry)
                            output_file.write(json.dumps(json_entry) + '\n')

def add_problem_type(file_name, json_entry):
    problem_type = None

    if json_entry["Answer Candidates"]:
        problem_type = "Multiple choice"
    elif "numerical" in file_name.lower():
        problem_type = "Numerical"
    elif "symbolic" in file_name.lower():
        problem_type = "Symbolic"
    elif "proof" in file_name.lower():
        problem_type = "Proof-like"

    if problem_type:
        json_entry["Problem Type"] = problem_type

    return json_entry

def main():
    input_dir = "/Users/tomohirosawada/Desktop/DUCK-datasets/final/data"
    output_dir = "/Users/tomohirosawada/Desktop/DUCK-datasets/final/data_revised"
    
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist. Please provide a valid directory.")
        return

    process_files(input_dir, output_dir)
    print("Processing completed successfully.")

if __name__ == "__main__":
    main()
