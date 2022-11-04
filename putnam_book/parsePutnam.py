import json
import markdown
import re
import pandas as pd

index_list = []
problem_dict = {}
num_probs = 935
bad_words = ["prove", "show", "cdn.mathpix.com"]
output = pd.DataFrame()
# output.columns=["Problem Number", "Problem Statement", "Solution", "Topic"]

letters = list("qwertyuiopasdfghjklzxcvbnm")

topic_list = ["Methods of Proof", "Algebra", "Real Analysis", "Geometry", "Number Theory", "Probability"]

topic_indexes = [80, 296, 572, 698, 905, 935]

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def parse_sections(text):
    index_list = list(find_all(text, "\subsection")) + list(find_all(text, "\subsubsection"))
    for i in range(1,num_probs+1):
        try:
            index_list.append(text.index("\n{}. ".format(i)))
        except:
            print("\n Error {}. ".format(i))
    index_list = list(sorted(index_list))

    text = [text[e:index_list[c+1]] for c,e in enumerate(index_list[:-1])]
    text = [e for e in text if "\subsection" not in e and "\subsubsection" not in e]

    problems = {}
    for problem in text:
        if not any([e in problem.lower() for e in bad_words]):
            num = problem.split('.')[0][1:]
            problems[int(num)] = problem
    return problems


with open("outputPutnam.csv", "w") as output_file, open("andreescu_putnam.md", 'r') as textfile:
    output_file.write("Pputnamroblem Number, Problem Statement, Solution, Final Answer")
    text = textfile.read()

    problems = text.split("\section{SOLUTIONS}")[0]
    solutions = text.split("\section{SOLUTIONS}")[1]

    problems = parse_sections(problems)
    solutions = parse_sections(solutions)

    for i in range(1,num_probs+1):
        if i in problems and i in solutions:
            output.at[i,0] = str(i)
            output.at[i,1] = problems[i]
            output.at[i,2] = solutions[i]
            output.at[i,3] = topic_list[max([c for c,e in enumerate(topic_indexes) if i <= topic_indexes[c]])]




output.columns=["Problem Number", "Problem Statement", "Solution", "Topic"]
output["Book"]   = ["Putnam and Beyond"]*len(output.index)
output["Final Answer"] = [""]*len(output.index)


js = output.to_json(orient="index")

with open('output.json', 'w') as f:
    f.write(js)

