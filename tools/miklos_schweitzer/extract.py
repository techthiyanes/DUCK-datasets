import os
import json
import re

def extract_problems_and_solutions(file_content):
    problems_and_solutions = []
    problem_pattern = r"Problem\s+([A-Za-z])\.1\.(.*?)Solution\."
    solution_pattern = r"Solution\.(.*?)(?:Problem\s+[A-Za-z]\.1\.|Solution\s+\d+|$)"

    problem_matches = re.finditer(problem_pattern, file_content, re.DOTALL)
    solution_matches = re.finditer(solution_pattern, file_content, re.DOTALL)

    for problem_match, solution_match in zip(problem_matches, solution_matches):
        problem_statement = problem_match.group(2).strip()
        solution = solution_match.group(1).strip()

        final_answer = re.search(r"([^=\n]*)(?=\s*\=*\s*\n|$)", solution, re.MULTILINE)
        if final_answer:
            final_answer = final_answer.group(1).strip()

        problems_and_solutions.append((problem_statement, solution, final_answer))

    return problems_and_solutions

def process_files_in_directory(input_directory, output_file):
    json_entries = []
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            with open(os.path.join(input_directory, filename), 'r') as file:
                content = file.read()
                problems_and_solutions = extract_problems_and_solutions(content)

                for problem_statement, solution, final_answer in problems_and_solutions:
                    json_entry = {
                        "Topic": os.path.splitext(filename)[0],
                        "Book": "Miklos Schweitzer Competitions",
                        "Problem Statement": problem_statement,
                        "Answer Candidates": [],
                        "Images": [],
                        "Output Format Instructions": "",
                        "Solution": solution,
                        "Final Answer": final_answer
                    }
                    json_entries.append(json_entry)

    with open(output_file, 'w') as outfile:
        for entry in json_entries:
            json.dump(entry, outfile)
            outfile.write('\n')

if __name__ == "__main__":
    input_directory = "/Users/tomohirosawada/Desktop/files"
    output_file = "output.jsonl"
    process_files_in_directory(input_directory, output_file)
