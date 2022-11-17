import regex as re
import pandas as pd
import json
import os

FILE = "barbri.txt"

file = open(FILE,"r").read()
file = file[:len(file)]


# eliminate errors
## eliminate images
regex_im = r"\!\[\]\(https:\/\/cdn\.mathpix\.com\/[A-Za-z\/0-9\_\-\.\?\=\&]+\)"
file = re.subn(regex_im,"",file)[0]

## eliminate newline error 
# regex_newline = r"\(D\)(.+?)[0-9]{2}\."
# file = re.findall(regex_im,file)

## Type 2 problems 
regex_type2 = r"Questions[, ]?([0-9]{1,3}\-[0-9]{1,3})"
file = re.subn(regex_type2,r"\n\n\\section{Questions \1}",file)[0]

## Missing newline and \section
regex_ns_inline = r"\(D\)(.+?)\. ([0-9]{1,3})\."
file = re.subn(regex_ns_inline,r"\n\n\\section{\1}",file)[0]
regex_ns = r"\n([0-9]{1,3})\."
file = re.subn(regex_ns,r"\n\n\\section{\1}",file)[0]



# split document 
## workshop testing drills
regex_prob1 = r"\\section\{THE FORM OF THE QUESTION\}(.+?)\\section\{CONSTITUTIONAL LAW ANSWERS\}"
problems_1 = re.search(regex_prob1,file,flags=re.DOTALL).group(1) 
regex_soln1 = r"\\section\{CONSTITUTIONAL LAW ANSWERS\}(.+?)\\section\{ANSWER SHEET \(MIXED SUBJECTS\)\}"
solutions_1 = re.search(regex_soln1,file,flags=re.DOTALL).group(1) 
with open('problems_1.txt', 'w') as f:
    f.write(problems_1)
with open('solutions_1.txt', 'w') as f:
    f.write(solutions_1)

## mixed subject questions
regex_prob2 = r"\\section\{ANSWER SHEET \(MIXED SUBJECTS\)\}(.+?)\\section\{ANSWER KEYAND SUBJECT MATTER KEY\}"
problems_2 = re.search(regex_prob2,file,flags=re.DOTALL).group(1) 
regex_soln2 = r"\\section\{ANSWER KEYAND SUBJECT MATTER KEY\}(.+?)\\title\{\nMultistate Practice Exam\n\}"
solutions_2 = re.search(regex_soln2,file,flags=re.DOTALL).group(1) 
with open('problems_2.txt', 'w') as f:
    f.write(problems_2)
with open('solutions_2.txt', 'w') as f:
    f.write(solutions_2)

## multistate practice exam
regex_prob3 = r"\\section\{ANSWER SHEET \(A.M. EXAM\)\}(.+?)\\section\{ANSWER KEY AND SUBJECT MATTER KEY\}"
problems_3 = re.search(regex_prob3,file,flags=re.DOTALL).group(1) 
regex_soln3 = r"\\section\{MULTISTATE PRACTICE EXAM ANALYTICAL ANSWERS\}(.+?)\\section\{CONSTITUTIONAL LAW QUESTIONS\}\n\n\\section\{Question 1\}"
solutions_3 = re.search(regex_soln3,file,flags=re.DOTALL).group(1) 
with open('problems_3.txt', 'w') as f:
    f.write(problems_3)
with open('solutions_3.txt', 'w') as f:
    f.write(solutions_3)

## released multistate questions
section_name_4 = [
    "CONSTITUTIONAL LAW", 
    "CONTRACTS", 
    "CRIMINAL LAW", 
    "EVIDENCE", 
    "REAL PROPERTY", 
    "TORTS"
]

problems_4    = []
solutions_4   = []

for i in range(len(section_name_4)): 
    regex_rmq_problems  = r"\\section\{"+ section_name_4[i] + r" QUESTIONS\}(.+?)\\section\{"+ section_name_4[i] + r" ANSWERS\}"
    if i<len(section_name_4)-1: 
        regex_rmq_solutions = r"\\section\{"+ section_name_4[i] + r" ANSWERS\}(.+?)\\section\{" + section_name_4[i+1] + r" QUESTIONS\}"
    else: 
        regex_rmq_solutions = r"\\section\{"+ section_name_4[i] + r" ANSWERS\}(.+?)"
    # txt = re.search(regex_rmq_problems,file,flags=re.DOTALL).group(1)
    result1 = re.search(regex_rmq_problems,file,flags=re.DOTALL)
    if result1: 
        result1 = result1.group(1)
        problems_4.append(result1)

    result2 = re.search(regex_rmq_solutions,file,flags=re.DOTALL)
    if result2: 
        result2 = result2.group(1)
        solutions_4.append(result2)
    with open("problems_4_" + section_name_4[i] +".txt", 'w') as f:
        f.write(problems_4[-1])
    with open("solutions_4_" + section_name_4[i] +".txt", 'w') as f:
        f.write(solutions_4[-1])






# Problems



def appendTypeII(problems,problist):
    # given string of problems `problems` and a list `problist`
    # find all Type II problems (i.e. multipart questions)
    # from `problems` and append them to problist
    problist_1mq = re.findall(regex_mq_problems,problems,flags=re.DOTALL)        
    for j in range(len(problist_1mq)): 
        elem1 = (problist_1mq[j][1], problist_1mq[j][0] + problist_1mq[j][2], problist_1mq[j][3])
        elem2 = (problist_1mq[j][4], problist_1mq[j][0] + problist_1mq[j][5], problist_1mq[j][6])
        problist.append(elem1)
        problist.append(elem2)
    return problist



## TYPE I: Common Multiple Choice Question
regex_cmcq = r"\\section\{Question ([0-9]+)\}(.+?)\(A\)(.+?)\\section\{" 
## TYPE II: Multipart Questions
regex_mq_problems = r"\\section\{Questions [0-9]{1,3}\-[0-9]{1,3}\} are based on the following fact situation:(.+?)\\section\{([0-9]{1,3})\}(.+?)\(A\)(.+?)\\section\{([0-9]{1,3})\}(.+?)\(A\)(.+?)\\section\{Question" 


### Working Testing Drills
section_name_1 = [
    "Constitutional Law", 
    "Contracts", 
    "Criminal Law", 
    "Evidence", 
    "Real Property", 
    "Torts"
]
problist_1   = re.findall(regex_cmcq,problems_1,flags=re.DOTALL,overlapped=True)
problist_1   = list(map(lambda x: [x[0],x[1],"(A) "+x[2]],problist_1))
problist_1   = appendTypeII(problems_1,problist_1)

count,current = 0,0

for i in range(len(problist_1)): 
    prev       = current
    current    = int(problist_1[i][0])
    if current < prev and count < len(section_name_1)-1: count += 1
    problist_1[i] = list(problist_1[i])
    problist_1[i][0] = str(section_name_1[count]) + " " + problist_1[i][0]
    problist_1[i] = tuple(problist_1[i])



# for i in range(len(problist_1)): 
#     prev       = current
#     current    = int(problist_1[i][0])
#     if current < prev and count < len(section_name_1)-1: count += 1
#     problist_1[i] = list(problist_1[i])
#     problist_1[i][0] = str(section_name_1[count]) + " " + problist_1[i][0]
#     problist_1[i] = tuple(problist_1[i])



# for i in range(len(problist_1)): 
#     prev       = current
#     current    = int(problist_1[i][0])
#     if current < prev and count < len(section_name_1)-1: count += 1
#     problist_1[i] = list(problist_1[i])
#     problist_1[i][0] = str(section_name_1[count]) + " " + problist_1[i][0]
#     problist_1[i] = tuple(problist_1[i])




### Mixed Subject Questions
problist_2 = re.findall(regex_cmcq,problems_2,flags=re.DOTALL,overlapped=True)
problist_2   = appendTypeII(problems_2,problist_2)
problist_2   = list(map(lambda x: ["Mixed Subj " + x[0],x[1],"(A) "+x[2]],problist_2))


### Multistate Practice Exam and Analytical Answers
section_name_3 = [
    "AM Exam",
    "PM Exam"
]
problist_3 = re.findall(regex_cmcq,problems_3,flags=re.DOTALL,overlapped=True)
problist_3   = appendTypeII(problems_3,problist_3)
problist_3   = list(map(lambda x: [x[0],x[1],"(A) "+x[2]],problist_3))


for i in range(len(problist_3)): 
    current    = int(problist_3[i][0])
    # print(current)
    if current < 101:
        problist_3[i][0] = str(section_name_3[0]) + " " + problist_3[i][0]
    else: 
        problist_3[i][0] = str(section_name_3[1]) + " " + problist_3[i][0]

### Released Multistate Questions and Analytical Answers

problist_4 = []

for i in range(len(problems_4)):
    lst = re.findall(regex_cmcq,problems_4[i],flags=re.DOTALL,overlapped=True)
    lst = appendTypeII(problems_4[i],lst)
    lst = list(map(lambda x: ["Multistate " + section_name_1[i]+" "+x[0],x[1],"(A) "+x[2]],lst))
    problist_4 += lst








# Solutions
regex_cmcq_soln = r"\\section\{Answer to Question ([0-9]+)\}[\n]+?\(([A-D])\)(.+?)\\section\{"

solnlist_1 = re.findall(regex_cmcq_soln,solutions_1,flags=re.DOTALL,overlapped=True)
solnlist_1 = list(map(list,solnlist_1))
count,current = 0,0

for i in range(len(solnlist_1)): 
    prev       = current
    current    = int(solnlist_1[i][0])
    if current < prev and count < len(section_name_1)-1: count += 1
    solnlist_1[i] = list(solnlist_1[i])
    solnlist_1[i][0] = str(section_name_1[count]) + " " + solnlist_1[i][0]
    solnlist_1[i] = tuple(solnlist_1[i])


solnlist_2 = re.findall(regex_cmcq_soln,solutions_2,flags=re.DOTALL,overlapped=True)
solnlist_2   = list(map(lambda x: ["Mixed Subj " + x[0],x[1],"(A) "+x[2]],solnlist_2))


solnlist_3 = re.findall(regex_cmcq_soln,solutions_3,flags=re.DOTALL,overlapped=True)
solnlist_3 = list(map(list,solnlist_3))
for i in range(len(solnlist_3)): 
    current    = int(solnlist_3[i][0])
    # print(current)
    if current < 101: 
        solnlist_3[i] = str(section_name_3[0]) + " " + solnlist_3[i][0]
    else: 
        solnlist_3[i] = str(section_name_3[1]) + " " + solnlist_3[i][0]


solnlist_4 = []
for i in range(len(solutions_4)):
    lst = re.findall(regex_cmcq_soln,solutions_4[i],flags=re.DOTALL,overlapped=True)
    lst = list(map(lambda x: ["Multistate " + section_name_1[i]+" "+x[0],x[1],x[2]],lst))
    solnlist_4 += lst




output = pd.DataFrame()
problst  = list(map(lambda x: list(map(list,x)),[problist_1, problist_2, problist_3, problist_4]))
solnlst  = list(map(lambda x: list(map(list,x)),[solnlist_1, solnlist_2, solnlist_3, solnlist_4]))



N = 0
for i in range(len(problst)): 
    solndct = {x[0]: x[1:] for x in solnlst[i]}
    keys    = solndct.keys() 
    for j in range(len(problst[i])): 
        n = problst[i][j][0]
        if n in keys: 
            N+= 1
            output = pd.concat([output,pd.DataFrame(problst[i][j] + solndct[n]).T])



output = pd.concat([output,pd.DataFrame(["Barbri Bar Review"]).T],axis=1)
output.columns = ["Problem Number", "Problem Statement", "Answer Choices","Final Answer", "Explanation", "Book Title"]
output.set_index(["Problem Number"])
output = output.sort_index()


with open("output.json", "w") as f:
    result = output.to_json(orient="records")
    parsed = json.loads(result)
    f.write(json.dumps(parsed,indent=4))


print(f"Number of problems: {len(output)}")
























