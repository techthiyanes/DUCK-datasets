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

def update_index(file='counter.txt',value=None,step='forward'): 
    # increase key in counter.txt
    # if value is specified, set key to value
    with open(file, 'r') as f:
        ind=int(f.read())
    if value:
        with open(file, 'w') as f:
            f.write(str(value))
    elif step=='backward':
        with open(file, 'w') as f:
            f.write(str(ind-1))
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
    # read key from counter.txt


    if request.args:
        ind = int(open('counter.txt', 'r').read())
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

        if request.args.get("next"):
            # use request.args.get(<name of input>) to 
            # add the input to the jsonl file
            
            update_index()

        elif request.args.get("previous"):
            if ind < 0:
                update_index()
            else: 
                update_index(step='backward')
        elif request.args.get("save"):
            append_jsonl(args.out_file, problem)
            update_index()
        else:
            update_index()
            raise ValueError("Unknown action")


    ind = int(open('counter.txt', 'r').read())

    if ind > len(input_file) - 1 or ind < 0:
        return "<p>There are no more problems!</p>"
    
    problem = input_file[ind]
    
    for field in PROBLEM_FIELDS:
        if field not in problem:
            problem[field] = ""

    if "Problem Number" in problem.keys():
        problem_number = problem["Problem Number"]
    else: 
        problem_number = "N/A"


    return render_template(
        "template.html",
        id=ind,
        topic=problem["Topic"],
        book=problem["Book"],
        problem_number = problem_number,
        problem_statement=problem["Problem Statement"],
        answer_candidates=list_to_str(problem["Answer Candidates"]),
        images=list_to_str(problem["Images"]),
        solution=problem["Solution"],
        final_answer=problem["Final Answer"],
        remaining_problems_cnt = len(input_file) - jsonl_length(output_file_name) - 1,
    )


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, required=True)
parser.add_argument('--out_file', type=str, required=True)
args = parser.parse_args()



if args.input_file.endswith(".jsonl"):
    input_file_name = args.input_file
    input_file = read_jsonl(args.input_file)
    output_file_name = args.out_file
    out_file = read_jsonl(args.out_file)
    
    with open(input_file_name, 'r') as json_file:
        json_list = list(json_file)


    for i in range(len(json_list)):
        json_str = json_list[i]
        result = json.loads(json_str)
        
        
else: 
    raise ValueError("Problems file must be JSONL file")




print("Reading problems from", input_file_name)
print("Write output to: {}".format(args.out_file))

if __name__ == "__main__":
    app.run(port=4000)
