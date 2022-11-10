import json
import re
import pandas as pd

index_list = []
problem_dict = {}
num_probs = 935
bad_words = ["prove", "show", "cdn.mathpix.com"]
output = pd.DataFrame()

letters = list("qwertyuiopasdfghjklzxcvbnm")
bad_unicode = "\u0941"
citation_keywords = ["olympiad", "proposed", "competition", "roegen", "communicated", "maa", "exam","contest", "problems", "examination", "mathematical", "mathematics", "matematic", "matematica", "gnedenko", "wiley", "rotkiewicz", "brahmagupta", "andreescu"]
topic_list = ["Methods of Proof", "Algebra", "Real Analysis", "Geometry", "Number Theory", "Probability"]

topic_indexes = [80, 296, 572, 698, 905, 935]

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def remove_irregularities(problem):
    problem = problem.replace("\n\n", "")
    problem = problem.translate({ord(x): '' for x in bad_unicode}) #remove bad unicode chars
    last_paren_open =  ([None] + list(find_all(problem, "(")))[-1]
    last_paren_close =  ([None] + list(find_all(problem, ")")))[-1]
    if last_paren_close and last_paren_open and any([citation in problem[last_paren_open:last_paren_close].lower() for citation in citation_keywords]):
        problem = problem[:last_paren_open] + problem[last_paren_close+1:]

    return problem


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
            problems[int(num)] = remove_irregularities(problem)
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

