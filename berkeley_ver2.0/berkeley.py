import re
import json
import pandas as pd
import sys

# File paths
toc_path = "berkeley_toc.txt"
problem_path = "problems.txt"
solution_path =  "solutions.txt"

toc = open(toc_path, "r")
toc = toc.read()
problems = open(problem_path, "r")
problems = problems.read()
solutions = open(solution_path, "r")
solutions = solutions.read()



# Fix formatting errors 

## Get rid of newline characters
# problems  = re.sub(r"\n",r" ",problems)
# solutions = re.sub(r"\n",r" ",solutions)

## \section{} for problem and solution numbers
regex_problem_section = r"\\section\{(Problem \d\.\d+\.\d+.+?)\}"
problems = re.sub(regex_problem_section,r"\1",problems)

regex_solution_section = r"\\section\{(Solution to \d\.\d+\.\d+.+?)\}"
solutions = re.sub(regex_solution_section,r"\1",solutions)

## eliminate \section and \subsection
### INSERT CODE HERE ###
regex_section = r"\\((sub)?section|title)\{[A-Za-z0-9\.\{\}\$\s\_\^\\]+?\}"
problems = re.sub(regex_section,r"",problems)
solutions = re.sub(regex_section,r"",solutions)




# topic name 
regex_toc = r"\$*(\d\.\d)\s*(\\quad)*\$* ([\w\s\',\{\}]+)"

toc_lst = re.findall(regex_toc,toc)
toc_dct = {num:name for (num,b,name) in toc_lst}
toc_num = set(toc_dct.keys())
toc_dct = pd.DataFrame(toc_dct,index=[0])


# produce dataframe of problems 
regex_problem_number = r"(Problem (\d\.\d\.\d*) \((Fa|Sp|Su)\d\d[\,? (Fa|Sp|Su)\d\d]*\))"
problist = re.split(regex_problem_number, problems)
problem_df = pd.DataFrame([problist[2::4],problist[4::4]])
problem_df = problem_df.T


# produce dataframe of solutions
regex_solution_number = r"(Solution to (\d\.\d\.\d*):)"
solnlist = re.split(regex_solution_number, solutions)
solution_df = pd.DataFrame([solnlist[2::3],solnlist[3::3]])
solution_df = solution_df.T





# Iterate over dataframe to look for computational problems

# Find computational problems
keywords = ["find","compute","calculate","evaluate","determine"]
keywords += list(map(lambda x: x.capitalize(), keywords))


for i in range(len(problem_df)):
  for j in range(len(keywords)):
    string = re.search(keywords[j],problem_df.loc[i][1])
    if string: break
  else: problem_df = problem_df.drop(i)

problem_df = problem_df.set_index([0])
solution_df = solution_df.set_index([0])
# print(problem_df.at["1.1.10",1])


problem_df[2] = pd.DataFrame([0]*len(problem_df[1]))

probnum = list(problem_df.index.values)
solnnum = set(solution_df.index.values)

for num in probnum: 
  if num in solnnum: 
    problem_df.at[num,2] = solution_df.at[num,1]



# eliminate solution 2
regex_soln2 = r"Solution 2. [\s\S]+"
problem_df[2] = problem_df[2].apply(lambda s: re.sub(regex_soln2,r"",str(s)))




# topic name
lst = list(map(lambda s: re.match(r"\d\.\d",s).group(0),problem_df.index.values))
problem_df[3] = toc_dct[lst].T.values

# print(problem_df)




# json file 
output = problem_df
output.columns=["Problem Statement", "Solution", "Topic"]
output["Book"]   = ["Berkeley Problems in Mathematics"]*len(output.index)
output["Final Answer"] = [""]*len(output.index)

js = output.to_json(orient="index")

with open('output.json', 'w') as f:
    f.write(js)




