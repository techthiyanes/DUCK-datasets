import argparse
import itertools
import json
import random
import pandas as pd

from flask import Flask, render_template, request


PROBLEM_FIELDS = [
    "Topic",
    "Book",
    "Problem Statement",
    "Answer Candidates",
    "Images",
    "Solution",
    "Final Answer",
]

# utils
def list_to_str(l):
    return "\n".join(l)

def str_to_list(s):
    l = [x.strip() for x in s.split("\n")]
    l = [x for x in l if x]
    return l

def read_jsonl(inp, l=None): 
    # read jsonl file 
    # return list of json objects
    # if line is specified, return the json object at that line
    json_list = []
    with open(inp, 'r') as f:
        for line in f:
            json_list.append(json.loads(line))
    if l:
        return json_list[l]
    else:
        return json_list
    
def write_jsonl(inp,line, key, value, output_file=None):
    # write jsonl file 
    # if line is specified, write the json object at that line
    # if output_file is not specified, overwrite input_file
    with open(inp, 'r') as f:
        json_objects = []
        for json_line in f:
            json_objects.append(json.loads(json_line))
    
    json_objects[line][key] = value
    
    if output_file: out = output_file
    else: out = inp

    with open(out, 'w') as f:
        for json_obj in json_objects:
            json.dump(json_obj, f)
            f.write('\n')

def append_jsonl(inp, json_obj, output_file=None):
    # append json object to jsonl file
    # if output_file is not specified, overwrite input_file
    if output_file: out = output_file
    else: out = inp
    with open(out, 'a') as f:
        json.dump(json_obj, f)
        f.write('\n')

def update_index(file='counter.txt',value=None): 
    # increase key in counter.txt
    # if value is specified, set key to value
    with open(file, 'r') as f:
        ind=int(f.read())
    if value:
        with open(file, 'w') as f:
            f.write(str(value))
    else: 
        with open(file, 'w') as f:
            f.write(str(ind+1))


def jsonl_length(file):
    # return length of jsonl file
    with open(file, 'r') as f:
        return sum(1 for line in f)
    



app = Flask(__name__)



@app.route("/")
def index(): 
    if request.args:
        problem = {
            "Topic": request.args.get("topic"),
            "Book": request.args.get("book"),
            "Problem Statement": request.args.get("problem_statement"),
            "Answer Candidates": request.args.get("answer_candidates"),
            "Images": request.args.get("images"),
            "Output Format Instructions": request.args.get("output_format_instructions"),
            "Solution": request.args.get("solution"),
            "Final Answer": request.args.get("final_answer"),
        }
        for field in problem:
            problem[field] = problem[field].replace("\r", "")
        problem["Answer Candidates"] = str_to_list(problem["Answer Candidates"])
        problem["Images"] = str_to_list(problem["Images"])

        # if not problem["Answer Candidates"]:
        #     problem.pop("Answer Candidates")
        # if not problem["Images"]:
        #     problem.pop("Images")

        if request.args.get("numerical"):
            # use request.args.get(<name of input>) to 
            # add the input to the jsonl file
            if problem["Images"]: 
                # add problem to numerical_images_file
                append_jsonl(args.numerical_images_file, problem)
                update_index()
            else: 
                # add problem to numerical_file
                append_jsonl(args.numerical_file, problem)
                update_index()
        elif request.args.get("symbolic"):
            if problem["Images"]: 
                # add problem to symbolic_images_file
                append_jsonl(args.symbolic_images_file, problem)
                update_index()
            else: 
                # add problem to symbolic_file
                append_jsonl(args.symbolic_file, problem)
                update_index()
        elif request.args.get("proof-based"):
            if problem["Images"]: 
                # add problem to proof_based_images_file
                if args.proof_based_images_file: 
                    append_jsonl(args.proof_based_images_file, problem)
                    update_index()
                else: 
                    return "<p>No proof-based problems with images file specified!</p>"
            else: 
                # add problem to proof_based_file
                if args.proof_based_file:
                    append_jsonl(args.proof_based_file, problem)
                    update_index()
                else: 
                    return "<p>No proof-based problems file specified!</p>"

        else:
            raise ValueError("Unknown action")

    # read key from counter.txt
    ind = int(open('counter.txt', 'r').read())

    if ind > len(input_file) - 1:
        return "<p>There are no more problems!</p>"
    
    problem = input_file[ind]
    
    for field in PROBLEM_FIELDS:
        if field not in problem:
            problem[field] = ""

    if args.proof_based_file: 
        proof_based_problems_cnt = jsonl_length(args.proof_based_file)
    else: 
        proof_based_problems_cnt = 0
    if args.proof_based_images_file:
        proof_based_problems_with_images_cnt = jsonl_length(args.proof_based_images_file)
    else:
        proof_based_problems_with_images_cnt = 0

    return render_template(
        "template.html",
        id=ind,
        topic=problem["Topic"],
        book=problem["Book"],
        problem_statement=problem["Problem Statement"],
        answer_candidates=list_to_str(problem["Answer Candidates"]),
        images=list_to_str(problem["Images"]),
        solution=problem["Solution"],
        final_answer=problem["Final Answer"],
        numerical_problems_cnt = jsonl_length(args.numerical_file),
        numerical_problems_with_images_cnt = jsonl_length(args.numerical_images_file),
        symbolic_problems_cnt = jsonl_length(args.symbolic_file),
        symbolic_problems_with_images_cnt = jsonl_length(args.symbolic_images_file),
        proof_based_problems_cnt = proof_based_problems_cnt,
        proof_based_problems_with_images_cnt = proof_based_problems_with_images_cnt,
        remaining_problems_cnt = len(input_file) - ind - 1,
    )


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, required=True)
parser.add_argument('--numerical_file', type=str, required=True)
parser.add_argument('--numerical_images_file', type=str, required=True)
parser.add_argument('--symbolic_file', type=str, required=True)
parser.add_argument('--symbolic_images_file', type=str, required=True)
parser.add_argument('--proof_based_file', type=str, required=False)
parser.add_argument('--proof_based_images_file', type=str, required=False)
# parser.add_argument('--show_images', action="store_true")
# parser.add_argument('--show_choices', action="store_true")
args = parser.parse_args()



if args.input_file.endswith(".jsonl"):
    input_file_name = args.input_file
    input_file = read_jsonl(args.input_file)
    numerical = read_jsonl(args.numerical_file)
    numerical_images = read_jsonl(args.numerical_images_file)
    symbolic = read_jsonl(args.symbolic_file)
    symbolic_images = read_jsonl(args.symbolic_images_file)
    if args.proof_based_file: 
        proof_based = read_jsonl(args.proof_based_file)
    if args.proof_based_images_file:
        proof_based_images = read_jsonl(args.proof_based_images_file)

    with open(input_file_name, 'r') as json_file:
        json_list = list(json_file)


    for i in range(len(json_list)):
        json_str = json_list[i]
        result = json.loads(json_str)
        
        
else: 
    raise ValueError("Problems file must be JSONL file")




print("Reading problems from", input_file_name)
print("Write numerical problems to: {}".format(args.numerical_file))
print("Writeg numerical images to: {}".format(args.numerical_images_file))
print("Write symbolic problems to: {}".format(args.symbolic_file))
print("Write symbolic images to: {}".format(args.symbolic_images_file))

if __name__ == "__main__":
    app.run()
