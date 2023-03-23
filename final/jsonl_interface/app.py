import argparse
import itertools
import json
import random
import pandas as pd
import os

from flask import Flask, render_template, request, redirect


PROBLEM_FIELDS = [
    "Topic",
    "Book",
    "Problem Statement",
    "Answer Candidates",
    "Images",
    "Solution",
    "Final Answer",
]

counter_file = "counter.txt"
current_file = "current_file.txt"

def list_to_str(l):
    return "\n".join(l)

def str_to_list(s):
    l = [x.strip() for x in s.split("\n")]
    l = [x for x in l if x]
    return l


app = Flask(__name__)



@app.route("/")
def index(): 
    with open(counter_file, 'r') as f:
        current_index=int(f.read())
    if request.args:
        if int(request.args.get("id")) != current_index:
            if  int(request.args.get("id")) >= 0 and int(request.args.get("id")) <= len(problem_dict):
                current_index = int(request.args.get("id"))
            else: 
                return "<p>There are no more problems!</p>"
        elif request.args.get("previous"):
            if current_index > 0:
                current_index -= 1
            else: 
                return "<p>There are no more problems!</p>"
        elif request.args.get("next"):
            if current_index < len(problem_dict)-1:
                current_index += 1
            else: 
                return "<p>There are no more problems!</p>"
        else:
            raise ValueError("Unknown action")

        with open(counter_file, 'w') as f:
                f.write(str(current_index))

        problem = {
            "Key": current_index, 
            "Topic": problem_dict[current_index]["Topic"],
            "Book": problem_dict[current_index]["Source"],
            "Problem Statement": problem_dict[current_index]["Problem Statement"],
            "Answer Candidates": problem_dict[current_index]["Answer Candidates"],
            "Images": problem_dict[current_index]["Images"],
            "Solution": problem_dict[current_index]["Solution"],
            "Final Answer": problem_dict[current_index]["Final Answer"],
        }

        return redirect("/")

    with open(counter_file, 'r') as f:
        current_index=int(f.read())
    key = list(problem_dict.keys())[current_index]
    problem = problem_dict[key]
    
    for field in PROBLEM_FIELDS:
        if field not in problem:
            problem[field] = ""

    return render_template(
        "template.html",
        id=current_index,
        topic=problem["Topic"],
        book=problem["Book"],
        problem_statement=problem["Problem Statement"],
        answer_candidates=list_to_str(problem["Answer Candidates"]),
        images=list_to_str(problem["Images"]),
        solution=problem["Solution"],
        final_answer=problem["Final Answer"],
        problem_dict_cnt=len(problem_dict),
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



if args.problems_file.endswith(".jsonl"):
    problems_file = args.problems_file
    if not os.path.exists(problems_file): 
        raise Exception('problems_file path does not exist!')

    with open(current_file, 'r') as c:
        if c != problems_file: 
            c = problems_file
            with open(counter_file, 'w') as f:
                f.write('0')
                f.close()

    with open(current_file, 'w') as f:
        f.write(c)
        f.close()




    with open(problems_file, 'r') as json_file:
        json_list = list(json_file)

    problem_dict = dict()

    for i in range(len(json_list)):
        json_str = json_list[i]
        result = json.loads(json_str)
        problem_dict.update({i: result})
        
elif args.problems_file.endswith(".json"):
    problems_file = args.problems_file
    problem_dict = json.load(open(problems_file, "r"))
else: 
    raise ValueError("Problems file must be JSON or JSONL file")

problem_keys = list(problem_dict.keys())

print("Reading problems from", problems_file)


app.run()