import re
import numpy as np
import json
import pandas as pd
import sys


def getSection(key):
    return str(key)[0:4]


def getProblemNumber(key):
    return str(key)[str(key).index("-") + 1:]


# File paths
toc_path = "markdown/brayman_kukush_toc.txt"
problem_path = "markdown/brayman_kukush_problems.txt"
solution_path = "markdown/brayman_kukush_solutions.txt"

toc = open(toc_path, "r")
toc = toc.read()
problems = open(problem_path, "r")
problems = problems.read()
solutions = open(solution_path, "r")
solutions = solutions.read()

sections_probs = [1995, 1996, 1997, 1998, 1999, 2000, 2000, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
                  2010, 2011, 2012, 2013, 2014, 2015, 2016, 2016]
sections_sols = [1995, 1996, 1997, 1998, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2009, 2010, 2011,
                 2012, 2013, 2014, 2015, 2016]

# Get rid of newline characters / fix formatting
problems = re.sub(r"\bSee.*", r" ", problems)
problems = re.sub(r"\n", r" ", problems)
solutions = re.sub(r"\n", r" ", solutions)

# problems
regex_prob = re.compile(r'(\d{1,2})\. (\(\d.{5,8}\))?( )?([A-Za-z].+?(?=(\d){1,2}\. ))')
probs_lst = regex_prob.finditer(problems)

# solutions
regex_sol = re.compile(r'(\d{1,2}) ([A-Z].+?Answer:(.+?)(?=(\$\.|\.)))')  # group 1 is the "answer"
sols_lst = regex_sol.finditer(solutions)

# answers
regex_answer = re.compile(r'Answer:.+?(?=(\$\.|\.))')
answer_lst = regex_answer.finditer(solutions)

dictionary = dict()

currentIndex = 0
maxIndex = 0
sectionIndex = 0
# Problem Statements
for match in probs_lst:
    currentIndex = int(match.group(1))
    if (currentIndex > maxIndex):
        maxIndex = currentIndex
    elif (currentIndex <= maxIndex and not str(match.group(4)).strip().__contains__("Prove that all its members are positive integers")):
        sectionIndex = sectionIndex + 1
        currentIndex = 0
        maxIndex = 0

    key = str(sections_probs[sectionIndex]) + "-" + match.group(1)
    if dictionary.get(key) is not None:
        value = dictionary.get(key)
    else:
        value = np.array(["", "", ""], dtype=object)
    value[0] = str(match.group(4)).strip()

    dictionary.update({key: value})

currentIndex = 0
maxIndex = 0
sectionIndex = 0
count = 0
# Solutions
sectionIndex = 0
for match in sols_lst:
    currentIndex = int(match.group(1))
    if (currentIndex > maxIndex
          and not str(match.group(2)).strip().__contains__("The set of points")):
        maxIndex = currentIndex
    elif (currentIndex <= maxIndex
          and not str(match.group(2)).strip().__contains__("Touching ellipses  ![]")
          and not str(match.group(2)).strip().__contains__("The set of points")
          and not str(match.group(2)).strip().__contains__("One can give other examples of a required norm")):
        sectionIndex = sectionIndex + 1
        currentIndex = 0
        maxIndex = 0

    key = str(sections_sols[sectionIndex]) + "-" + match.group(1)
    if (dictionary.get(key) is not None):
        value = dictionary.get(key)
    else:
        value = np.array(["", "", ""], dtype=object)
    value[1] = str(match.group(2)).strip()
    value[2] = str(match.group(3)).strip()

    dictionary.update({key: value})

# Removes all key-value pairs where we don't have both the problem statement and the solution
dictionary = {key: value for key, value in dictionary.items() if (value[0] != "" and value[1] != "")}

for key in dictionary:
    print(key)
    print(dictionary.get(key))
    print()

output = pd.DataFrame()

key_counter = 0
for key in dictionary:
    problemNumber = getProblemNumber(key)
    section = getSection(key)
    output.at[key_counter, 0] = problemNumber
    output.at[key_counter, 1] = dictionary.get(key)[0]
    output.at[key_counter, 2] = dictionary.get(key)[1]
    output.at[key_counter, 3] = dictionary.get(key)[2]
    output.at[key_counter, 4] = section
    key_counter = key_counter + 1

output.columns = ["Problem Number", "Problem Statement", "Solution", "Final Answer", "Topic"]
output["Book"] = ["Brayman Kukush Undergraduate Mathematics Competitions (1995–2016)"] * len(output.index)

js = output.to_json(orient="index")

with open('output.json', 'w') as f:
    f.write(js)