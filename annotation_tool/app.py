import argparse
import itertools
import json
import random

from flask import Flask, render_template, request, redirect


PROBLEM_FIELDS = [
    "Topic",
    "Book",
    "Problem Statement",
    "Problem Choices",
    "Images",
    "Solution",
    "Final Answer",
]

def list_to_str(l):
    return "\n".join(l)

def str_to_list(s):
    l = [x.strip() for x in s.split("\n")]
    l = [x for x in l if x]
    return l


app = Flask(__name__)

@app.route("/")
def index():
    if request.args:
        key = request.args.get("id")
        problem = {
            "Topic": request.args.get("topic"),
            "Book": request.args.get("book"),
            "Problem Statement": request.args.get("problem_statement"),
            "Problem Choices": request.args.get("problem_choices"),
            "Images": request.args.get("images"),
            "Solution": request.args.get("solution"),
            "Final Answer": request.args.get("final_answer"),
        }
        for field in problem:
            problem[field] = problem[field].replace("\r", "")
        problem["Problem Choices"] = str_to_list(problem["Problem Choices"])
        problem["Images"] = str_to_list(problem["Images"])
        
        if not problem["Problem Choices"]:
            problem.pop("Problem Choices")
        if not problem["Images"]:
            problem.pop("Images")

        if request.args.get("accept"):
            final_problems[key] = problem
            remaining_problems.pop(key)
            json.dump(final_problems, open(args.final_problems_file, "w"), indent=4)
        elif request.args.get("reject"):
            rejected_problems[key] = problem
            remaining_problems.pop(key)
            json.dump(rejected_problems, open(args.rejected_problems_file, "w"), indent=4)
        elif request.args.get("skip"):
            remaining_problems[key] = problem
        else:
            raise ValueError("Unknown action")
        
        return redirect("/")

    if not remaining_problems:
        return "<p>There are no more problems!</p>"

    key = random.choice(list(remaining_problems.keys()))
    problem = remaining_problems[key]
    
    for field in PROBLEM_FIELDS:
        if field not in problem:
            problem[field] = ""

    return render_template(
        "template.html",
        id=key,
        topic=problem["Topic"],
        book=problem["Book"],
        problem_statement=problem["Problem Statement"],
        problem_choices=list_to_str(problem["Problem Choices"]),
        images=list_to_str(problem["Images"]),
        solution=problem["Solution"],
        final_answer=problem["Final Answer"],
        accepted_problems_cnt=len(final_problems),
        accepted_problems_with_images_cnt=len([p for p in final_problems.values() if "Images" in p and p["Images"]]),
        rejected_problems_cnt=len(rejected_problems),
        remaining_problems_cnt=len(remaining_problems),
        show_images=args.show_images,
        show_choices=args.show_choices,
    )

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


parser = argparse.ArgumentParser()
parser.add_argument('--problems_file', type=str, required=True)
parser.add_argument('--final_problems_file', type=str)
parser.add_argument('--rejected_problems_file', type=str)
parser.add_argument('--show_images', action="store_true")
parser.add_argument('--show_choices', action="store_true")
args = parser.parse_args()

if not args.problems_file.endswith(".json"):
    raise ValueError("Problems file must be a JSON file")
if not args.final_problems_file:
    args.final_problems_file = args.problems_file[:-5] + "_final.json"
if not args.rejected_problems_file:
    args.rejected_problems_file = args.problems_file[:-5] + "_rejected.json"

print("Reading problems from", args.problems_file)
print("Final problems will be stored to", args.final_problems_file)
print("Rejected problems will be stored to", args.rejected_problems_file)

remaining_problems = json.load(open(args.problems_file, "r"))
try:
    final_problems = json.load(open(args.final_problems_file, "r"))
except FileNotFoundError:
    final_problems = {}
try:
    rejected_problems = json.load(open(args.rejected_problems_file, "r"))
except FileNotFoundError:
    rejected_problems = {}

for key in itertools.chain(final_problems.keys(), rejected_problems.keys()):
    if key in remaining_problems:
        remaining_problems.pop(key)

app.run()