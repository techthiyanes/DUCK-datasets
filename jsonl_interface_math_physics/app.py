import argparse
import itertools
import json
import random
import pandas as pd
import os
import jsonlines

from flask import Flask, render_template, request, redirect


PROBLEM_FIELDS = [
    "Topic",
    "Book",
    "Problem Statement",
    "Answer Candidates",
    "Images",
    "Solution",
    "Final Answer",
    "Output Format Instructions"
]

counter_file = "counter.txt"
current_file = "current_file.txt"
remaining_problems_file = "remaining_problems.jsonl"
numerical_problems_file = "numerical.jsonl"
numerical_problems_w_images_file = "numerical_w_images.jsonl"
symbolic_problems_file = "symbolic.jsonl"
symbolic_problems_w_images_file = "symbolic_w_images.jsonl"



def list_to_str(l):
    return "\n".join(l)

def str_to_list(s):
    l = [x.strip() for x in s.split("\n")]
    l = [x for x in l if x]
    return l


def open_jsonl(file): 
    # open jsonl file as dict 
    with open(file, 'r') as json_file:
        json_list = list(json_file)

    output = dict()

    for i in range(len(json_list)):
        json_str = json_list[i]
        result = json.loads(json_str)
        output.update({i: result})
    return output

def append_jsonl(file, data):
    # append dict to jsonl file
    # Open the file in append mode
    with open(file, 'a') as f:

        # Serialize the dictionary to a JSON string
        json_data = json.dumps(data)

        # Write the serialized JSON string to the file
        f.write(json_data + '\n')

        # Close the file
        f.close()

def json_file_to_dict(file_path):
    with open(file_path, 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
    return data

def pop_jsonl(file_path, key=0):
    # create a temporary file to write the modified records
    temp_file_path = file_path + '.temp'
    with jsonlines.open(file_path, 'r') as reader, \
         jsonlines.open(temp_file_path, 'w') as writer:
        for record in reader:
            # remove the key from the record
            if key in record:
                del record[key]
            # write the modified record to the temporary file
            writer.write(record)
    # replace the original file with the temporary file
    os.replace(temp_file_path, file_path)

def write_jsonl(file,string): 
    # write jsonl file with string
    with open(file, "w") as g: 
            g.write(string)
            g.close()


app = Flask(__name__)



@app.route("/")
def index(): 
    with open(counter_file, 'r') as f:
        key=int(f.read())
    if request.args:
        problem = {
            "Problem Number": remaining_problems[key]["Problem Number"],
            "Topic": remaining_problems[key]["Topic"],
            "Book": remaining_problems[key]["Source"],
            "Problem Statement": request.args.get("problem_statement"),
            "Answer Candidates": request.args.get("answer_candidates"),
            "Output Format Instructions": request.args.get("output_format_instruction"),
            "Images": request.args.get("images"),
            "Solution": request.args.get("solution"),
            "Final Answer": request.args.get("final_answer"),
        }
        if request.args.get("previous"):
            if key > 0:
                key -= 1
            else: 
                return "<p>There are no more problems!</p>"
        elif request.args.get("next"):
            if key < len(remaining_problems)-1:
                key += 1
            else: 
                return "<p>There are no more problems!</p>"
        elif request.args.get("numerical"):
            numerical_problems[key] = problem
            remaining_problems.pop(key)
            pop_jsonl(remaining_problems_file)
            append_jsonl(numerical_problems_file, problem)
        elif request.args.get("numerical_images"):
            numerical_problems_w_images[key] = problem
            remaining_problems.pop(key)
            pop_jsonl(remaining_problems_file)
            append_jsonl(numerical_problems_w_images_file, problem)
            # json.dump(numerical_problems_w_images, open(numerical_problems_w_images_file, "w"), indent=4)
        elif request.args.get("symbolic"):
            symbolic_problems[key] = problem
            remaining_problems.pop(key)
            pop_jsonl(remaining_problems_file)
            append_jsonl(symbolic_problems_file, problem)
            # json.dump(symbolic_problems, open(symbolic_problems_file, "w"), indent=4)
        elif request.args.get("symbolic_images"):
            symbolic_problems_w_images[key] = problem
            remaining_problems.pop(key)
            pop_jsonl(remaining_problems_file)
            append_jsonl(symbolic_problems_w_images_file, problem)
            # json.dump(symbolic_problems_w_images, open(symbolic_problems_w_images_file, "w"), indent=4)
        else:
            raise ValueError("Unknown action")

        with open(counter_file, 'w') as f:
                f.write(str(key+1))

        return redirect("/")

    with open(counter_file, 'r') as f:
        key=int(f.read())
    key = list(remaining_problems.keys())[key]
    problem = remaining_problems[key]
    
    for field in PROBLEM_FIELDS:
        if field not in problem:
            problem[field] = ""

    return render_template(
        "template.html",
        id=problem["Problem Number"],
        topic=problem["Topic"],
        book=problem["Book"],
        problem_statement=problem["Problem Statement"],
        answer_candidates=list_to_str(problem["Answer Candidates"]),
        images=list_to_str(problem["Images"]),
        solution=problem["Solution"],
        output_format_instructions=problem["Output Format Instructions"],
        final_answer=problem["Final Answer"],
        numerical_problems_cnt = len(numerical_problems), 
        numerical_problems_with_images_cnt = len(numerical_problems_w_images), 
        symbolic_problems_cnt  = len(symbolic_problems), 
        symbolic_problems_with_images_cnt = len(symbolic_problems_w_images), 
        remaining_problems_cnt = len(remaining_problems), 
        problem_dct_cnt=len(remaining_problems),
        show_images=args.show_images,
        show_choices=args.show_choices,
    )


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


parser = argparse.ArgumentParser()
parser.add_argument('--problems_file', type=str, required=True)
parser.add_argument('--show_images', action="store_true")
parser.add_argument('--show_choices', action="store_true")
args = parser.parse_args()



problems_file = args.problems_file
print("Reading problems from", problems_file)
print("Numerical problems will be stored to", numerical_problems_file)
print("Numerical problems with images will be stored to", numerical_problems_w_images_file)
print("Symbolic problems will be stored to", symbolic_problems_file)
print("Symbolic problems with images will be stored to", symbolic_problems_w_images_file)



with open(current_file, "r") as f: 
    string = f.read()
    if string != problems_file: 
        string = problems_file
        with open(counter_file, "w") as c: 
            c.write("0")
            c.close()
        # write_jsonl(remaining_problems_file, open_jsonl(problems_file))
        write_jsonl(numerical_problems_file, str({}))
        write_jsonl(numerical_problems_w_images_file,  str({}))
        write_jsonl(symbolic_problems_file,  str({}))
        write_jsonl(symbolic_problems_w_images_file,  str({}))
    f.close()

with open(current_file, "w") as f: 
    f.write(string)
    f.close()


remaining_problems = open_jsonl(remaining_problems_file)
# make sure the problems file is the same as the one we're using
if not remaining_problems: 
    remaining_problems = open_jsonl(problems_file)



try:
    numerical_problems = open_jsonl(numerical_problems_file)
except FileNotFoundError:
    numerical_problems = {}
try:
    numerical_problems_w_images = open_jsonl(numerical_problems_w_images_file)
except FileNotFoundError:
    numerical_problems_w_images = {}
try:
    symbolic_problems = open_jsonl(symbolic_problems_file)
except FileNotFoundError:
    symbolic_problems = {}
try:
    symbolic_problems_w_images = open_jsonl(symbolic_problems_w_images_file)
except FileNotFoundError:
    symbolic_problems_w_images = {}







app.run()