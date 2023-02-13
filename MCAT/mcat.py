import json
import markdown
import re
import pandas as pd
from itertools import count, filterfalse
import urllib.request

output = pd.DataFrame()

remove_list = ["\n\nFoundations of Living Systems MCAT\n\n", "Answers and Explanations MCAT"]

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


    broken_text = [text[e:index_list[c+1]] for c,e in enumerate(index_list[:-1])]
    
    if len(index_list) > 0:
        broken_text.append(text[index_list[-1]:])

    questions = {int(e.split('.')[0]) : '.'.join(e.split('.')[1:]).strip().replace("\n\n\n",'\n').replace("\n\n",'\n').strip('\n') for e in broken_text if "Questions " not in e and "STOP." not in e}
    passages = [e for e in broken_text if "Questions " in e]

    for passage in passages:
        if '-' in passage:
            question_numbers = list((lambda start, end: range(int(start), int(end)+1))(*next(e for e in passage.split(" ") if "-" in e).split('-')))
            for question in question_numbers:
                if len(questions[question])>5:
                    questions[question] = passage.strip().replace("\n\n\n",'\n').replace("\n\n",'\n').strip('\n') + "\n" + questions[question]
                else:
                    del questions[question]
    
    return questions


def clean(text):
    return text.replace("Practice Test 1 ", "").replace("Practice Test 2 ", "").replace("Practice Test 3 ", "").replace("SECTION 3:\nPsychological,\nSocial, and\nBiological\nFoundations\nof Behavior MCAT"," ").replace("SECTION 3:\nPsychological,\nSocial, and\nBiological\nFoundations of Behavior", " ")

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

    answers = {int(e.split('.')[0]) : e.strip() for e in broken_text}
    
    return answers


def filter_answer_links(x):
    try:
        return 'http' in x.split("A.")[1]
    except Exception as e:
        print("AHHHH")
        print(x)



questions = {}

for number in ["1", "2", "3"]:
    with open("test_{}.txt".format(number), 'r') as problems:
        problems = problems.read()
        problems = problems.strip().replace("\n\n\n",'\n').replace("\n\n",'\n').strip('\n')
        problems = clean(problems)
        problems, solutions = problems.split("\section{ANSWERS AND EXPLANATIONS}")
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
                    continue_flag = False
                    if filter_answer_links(problem_dict[problem]):
                        continue

                    # get links of problem
                    link = [e[4:-1] for e in problem_dict[problem].split('A. ')[0].replace("\n", " ").split(" ") if "https" in e] if "https" in problem_dict[problem] else []
                    for c,url in enumerate(link):
                        try:
                            url = url.split(")")[0]
                            urllib.request.urlretrieve(url, f"{number}_{c}_{problem}_{c}.jpg")
                            link[c] = f"{number}_{c}_{problem}_{c}.jpg"
                        except:
                            print("ERROR URL")
                            continue_flag = True
                    if continue_flag:
                        continue

                    
                    # get remove first link from problem
                    problem_dict[problem] = '\n'.join(filterfalse(lambda L, c=count(): 'https' in L and next(c) < len(link), problem_dict[problem].split('\n'))) if "https" in problem_dict[problem] else problem_dict[problem]

                    # get remove answers
                    problem_choices = re.split(r'\nA. +|\nB. +|\nC. +|\nD. ', problem_dict[problem])[-4:]
                    problem_dict[problem] = re.split(r'\nA. +|\nB. +|\nC. +|\nD. ', problem_dict[problem])[0]


                    if "passage.\n" in problem_dict[problem]:
                        problem_dict[problem] = problem_dict[problem].split("passage.\n")[1].strip()

                    # add row to dataframe

                    if "\begin{tabular}" in problem_dict[problem] or "mathpix" in problem_dict[problem] or len(problem_dict[problem]) < 20:
                        continue
                    new_row = {"Problem Number" : f"{number}_{c}_{problem}", "Problem Statement" : problem_dict[problem], "Answer Candidates" : problem_choices,  "Images" : link, "Topic": topic, "Source" : f"MCAT_{number}", "Solution" : "", "Final Answer" : ""}
                    output = output.append(new_row, ignore_index = True)

                    questions[f"{number}_{c}_{problem}"] = problem_dict[problem]

        for c,section in enumerate(answer_sections):
            print(c)
            sol_dict = parse_solution(section)
            for sol in sol_dict:
                # add row to dataframe
                print(f"{number}_{c}_{sol}")

                output.loc[output['Problem Number'] == f"{number}_{c}_{sol}", 'Solution'] = sol_dict[sol]

                final_ans = next(e for e in reversed(sol_dict[sol].split("The correct answer is ")[1].split(".")[0]) if e in "QWERTYUIOPLKJHGFDSAZXCVBNM")
                output.loc[output['Problem Number'] == f"{number}_{c}_{sol}", 'Final Answer'] = final_ans

# note to self, this does not work rn need to filter by answer
# currently is none, need to skip adding solutions when there is no row for that solution

#output = output[output['Problem Statement'].map(filter_answer_links)]

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

# print(output.loc[100, :].values.tolist())
output.set_index("Problem Number")
js = output.to_json(orient="index")

with open('output.json', 'w') as f:
    f.write(js)


# ignore if anwer in the problem has images