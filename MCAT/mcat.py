import json
import markdown
import re
import pandas as pd
from itertools import count, filterfalse

output = pd.DataFrame()

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


# gets a dict of the questions from a section
def parse_section(text):
    index_list = list(find_all(text, "Questions ")) + list(find_all(text, "STOP."))
    for i in count(1):
        try:
            index_list.append(text.index("\n{}. ".format(i)))
        except:
            try:
                index_list.append(text.index(" {}. ".format(i)))
            except:
                break
    index_list = list(sorted(index_list))
    print(index_list)
    print("INDEX LIST ST ST ST______ \n\n\n\n")

    broken_text = [text[e:index_list[c+1]] for c,e in enumerate(index_list[:-1])]
    
    if len(index_list) > 0:
        broken_text.append(text[index_list[-1]:])

    questions = {int(e.split('.')[0]) : e for e in broken_text if "Questions " not in e and "STOP." not in e}
    passages = [e for e in broken_text if "Questions " in e]

    print('\n\n\nYEEEAST'.join(broken_text))
    for passage in passages:
        if '-' in passage:
            question_numbers = list((lambda start, end: range(int(start), int(end)+1))(*next(e for e in passage.split(" ") if "-" in e).split('-')))
            for question in question_numbers:
                questions[question] = passage + "\n" + questions[question]
    
    return questions


def clean(text):
    return text.replace("Practice Test 1 ", "").replace("Practice Test 2 ", "").replace("Practice Test 3 ", "")    

def parse_solution(text):
    index_list = []

    for i in count(1):
        try:
            index_list.append(text.index("\n{}. ".format(i)))
        except Exception as e:
            try:
                index_list.append(text.index(" {}. ".format(i)))
            except:
                break
    
    broken_text = [text[e:index_list[c+1]] for c,e in enumerate(index_list[:-1])]
    if len(index_list) > 0:
        broken_text.append(text[index_list[-1]:])

    answers = {int(e.split('.')[0]) : e for e in broken_text}
    
    return answers






questions = {}

for number in ["1", "2", "3"]:
    with open("test_{}.txt".format(number), 'r') as problems:
        problems, solutions = problems.read().split("\section{ANSWERS AND EXPLANATIONS}")
        sections = [clean(e) for e in problems.split("This is the end")]
        answer_sections = [clean(e) for e in solutions.split("\section{Section") if not len(e) < 20]

        
        topic = "MCAT Science"
        for c,section in enumerate(sections):
            print(c)

            # swich topic when we reach mcat reading section
            if "Critical Analysis and Reasoning Skills" in section:
                topic = "MCAT Reading"
            
            if "of Section" not in section or not len(section) < 20:
                #print(section[0:1000])
                problem_dict = parse_section(section)
                for problem in problem_dict:
                    # get links of problem
                    link = [e[4:-1] for e in problem_dict[problem].split('A. ')[0].replace("\n", " ").split(" ") if "https" in e] if "https" in problem_dict[problem] else []
                    
                    # get remove first link from problem
                    problem_dict[problem] = '\n'.join(filterfalse(lambda L, c=count(): 'https' in L and next(c) < len(link), problem_dict[problem].split('\n'))) if "https" in problem_dict[problem] else problem_dict[problem]

                    # add row to dataframe
                    new_row = {"Problem Number" : f"{number}_{c}_{problem}", "Problem Statement" : problem_dict[problem], "Image" : link, "Topic": topic, "Book" : f"MCAT_{number}", "Solution" : ""}
                    output = output.append(new_row, ignore_index = True)

                    questions[f"{number}_{c}_{problem}"] = problem_dict[problem]

        for c,section in enumerate(answer_sections):
            print(c)
            sol_dict = parse_solution(section)
            for sol in sol_dict:
                # add row to dataframe
                print(f"{number}_{c}_{sol}")
                output.loc[output['Problem Number'] == f"{number}_{c}_{sol}", 'Solution'] = sol_dict[sol]






output["Final Answer"] = [""]*len(output.index)

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

# print(output.loc[100, :].values.tolist())
output.set_index("Problem Number")
js = output.to_json(orient="index")

with open('output.json', 'w') as f:
    f.write(js)


# ignore if answer has images