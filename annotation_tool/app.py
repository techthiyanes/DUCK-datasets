import argparse
import json
import random

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    if request.args:
        key = request.args.get("id")
        problem = {
            "Topic": request.args.get("topic"),
            "Book": request.args.get("book"),
            "Problem Statement": request.args.get("problem_statement"),
            "Solution": request.args.get("solution"),
            "Final Answer": request.args.get("final_answer"),
        }
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

    if not remaining_problems:
        return "<p>There are no more problems!</p>"

    key = random.choice(list(remaining_problems.keys()))
    problem = remaining_problems[key]

    return render_template(
        "template.html",
        id=key,
        topic=problem["Topic"],
        book=problem["Book"],
        problem_statement=problem["Problem Statement"],
        solution=problem["Solution"],
        final_answer=problem["Final Answer"],
    )

parser = argparse.ArgumentParser()
parser.add_argument('--problems_file', type=str, required=True)
parser.add_argument('--final_problems_file', type=str)
parser.add_argument('--rejected_problems_file', type=str)
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

for key in final_problems:
    remaining_problems.pop(key)
for key in rejected_problems:
    remaining_problems.pop(key)

app.run()