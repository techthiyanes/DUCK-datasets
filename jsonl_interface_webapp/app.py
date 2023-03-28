# import argparse
import itertools
import json
import random
import pandas as pd
import os

from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session


PROBLEM_FIELDS = [
    "Topic",
    "Source",
    "Problem Statement",
    "Answer Candidates",
    "Images",
    "Solution",
    "Final Answer",
]

counter_file = "counter.txt"
current_file = "current_file.txt"
problems_path = "cache/numerical.jsonl"


def list_to_str(l):
    return "\n".join(l)

def str_to_list(s):
    l = [x.strip() for x in s.split("\n")]
    l = [x for x in l if x]
    return l


app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with the same secret key used in initialize.py
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route("/")
def index():     
    with open(counter_file, 'r') as f:
        current_index=int(f.read())
    if request.args:  
        if request.args.get("id") and int(request.args.get("id")) != current_index:
            if int(request.args.get("id")) >= 0 and int(request.args.get("id")) <= len(problem_dict):
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
            "Source": problem_dict[current_index]["Source"],
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
        Source=problem["Source"],
        problem_statement=problem["Problem Statement"],
        answer_candidates=list_to_str(problem["Answer Candidates"]),
        images=list_to_str(problem["Images"]),
        solution=problem["Solution"],
        final_answer=problem["Final Answer"],
        problem_dict_cnt=len(problem_dict),
        show_images=showimages,
        show_choices=showchoices,
    )


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

showimages = True
showchoices = True

@app.before_request
def before_request():
    # retrieve problems path from session
    if session and 'problems_path' in session: 
        problems_path = session['problems_path']
        print(f"Loading problems from {problems_path}")

    # load problems from file
    if problems_path.endswith(".jsonl"):
        if not os.path.exists(problems_path): 
            raise Exception('problems_path path does not exist!')

        with open(current_file, 'r') as c:
                cf = c.read()
                if cf != problems_path: 
                    cf = problems_path
                    with open(counter_file, 'w') as f:
                        f.write('0')
                        f.close()
                    with open(current_file, 'w') as c:
                        c.write(cf)
                        c.close()
                c.close()

        

        # generate list of json objects containing problems
        json_list = []
        line_count = 0
        print(f"Loading problems... {problems_path}")
        with open(problems_path, 'r') as file:
            for line in file:
                try:
                    json.loads(line)
                    json_list.append(line)
                    line_count += 1
                except json.JSONDecodeError:
                    print(f"Invalid JSON object at line {line_count + 1}")
                    continue

        global problem_dict
        problem_dict = dict()

        for i in range(len(json_list)):
            json_str = json_list[i]
            result = json.loads(json_str)
            problem_dict.update({i: result})

    else: 
        raise ValueError("Problems file must be JSONL file")

    global problem_keys
    problem_keys = list(problem_dict.keys())    

app.run(port=5001, debug=True)