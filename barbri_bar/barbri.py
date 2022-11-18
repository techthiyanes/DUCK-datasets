import regex as re
import pandas as pd
import json
import os

FILE = "barbri.txt"

file = open(FILE,"r").read()
file = file[:len(file)]

dirname = os.path.dirname(__file__) + "/assets/"


# clean document 

## Typos

regexes_clean = [
    [r"\!\[\]\(https:\/\/cdn\.mathpix\.com\/[A-Za-z\/0-9\_\-\.\?\=\&]+\)",r""],  ## eliminate images
    [r"Questions[, ]?([0-9]{1,3}\-[0-9]{1,3})",r"\n\n\\section{Questions \1}"], ## Type 2 problems 
    [r"\(D\)(.+?)\. ([0-9]{1,3})\.",r"\n\n\\section{\1}"], ## Missing newline and \section
    [r"\n([0-9]{1,3})\.",r"\n\n\\section{\1}"], ## Missing newline and \section
    [r"KEYAND", r"KEY AND"], 
    [r"\$\\\$",r"\$"], 
    [r"\\\\\$", r"\$"]
]

for i in range(len(regexes_clean)): 
    file = re.subn(regexes_clean[i][0],regexes_clean[i][1],file)[0]

with open(os.path.join(dirname,"modified.txt"),"w") as f: 
    f.write(file)



# split into sections
regexes = [
    r"\\section{Constitutional Law}\n\n(\\section\{Question 1\}\n\nSt\. Minny\, a town.+?)which is what happened here.", # WTD
    r"(\\section{Question 1}\n\nOswald owned an old, unoccupied,.+?)\\title\{\nMultistate Practice Exam\n\}",  # MSQ
    r"(\\section\{Question 1\}\n\nDennis robbed a bank.+?)\\section\{CONSTITUTIONAL LAW QUESTIONS\}\n\n\\section\{Question 1\}\n\nA newly enacted criminal statute provides", # MPE
    # part 4
    r"\\section\{CONSTITUTIONAL LAW QUESTIONS\}\n\n(\\section\{Question 1\}.+?)\\section\{CONTRACTS QUESTIONS\}", # CONSTITUTIONAL LAW QUESTIONS
    r"The contract has no provision regarding assignment.(.+?)\\section\{CRIMINAL LAW QUESTIONS\}", # CONTRACTS QUESTIONS
    r"\\section\{CRIMINAL LAW QUESTIONS\}\n\n\\section{Question 1}\n\n(In which of the following situations is Defendant's claim.+?)\\section\{EVIDENCE QUESTIONS\}",# CRIMINAL LAW QUESTIONS
    r"(\\section\{Questions 1-2\} are based on the following fact situation:\n\nPaula sued for injuries she sustained.+?)\\section\{REAL PROPERTY QUESTIONS\}", # EVIDENCE QUESTIONS
    r"(\\section\{Questions 1-3\} are based on the following fact situation:\n\nSue owned a five-acre.+?)\\section\{TORTS QUESTIONS\}",
    r"(\\section\{Questions 1-2\} are based on the following fact situation:\n\nInnes worked as a.+?)\\section\{MDR 2007\}"
]

sections = []

for i in range(len(regexes)):
    regex = regexes[i]
    sections.append(re.search(regex,file,flags=re.DOTALL).group(0))
    with open(os.path.join(dirname + f"sections_{i}.txt"),"w") as f: 
        f.write(sections[-1])



# functions for extracting problem and solution
labels = [
    [
    "WTD Constitutional Law", 
    "WTD Contracts", 
    "WTD Criminal Law", 
    "WTD Evidence", 
    "WTD Real Property", 
    "WTD Torts"], 
    ["MSQ"]*6, 
    ["AM Exam", 
    "PM Exam"], 
    ["RMQ Constitutional Law"],
    ["RMQ Contracts"],
    ["RMQ Criminal Law"], 
    ["RMQ Evidence"], 
    ["RMQ Real Property"], 
    ["RMQ Torts"]
]

def applyLabels(output,n): 
    # given list of [problem number, statement, and choices]
    # return list with problem number labeled by `labels`
    # n is the index in `sections`
    counter, current = 0, int(output[0][0])
    if len(labels[n]) == 1: 
        for i in range(len(output)):
            output[i][0] = labels[n][0] + " " + output[i][0]
    else:
        for i in range(len(output)): 
            prev    = current
            current = int(output[i][0].strip())
            if prev > current: counter += 1
            output[i][0] = labels[n][counter] + " " + output[i][0]
    return output 

def problemExtract(string,n): 
    # given string with problems and section number
    # return list of lists with problem number, statement, and choices
    # with correct labeling for problem num
    regex  = r"\\section\{Question ([0-9]{1,3})\}(.+?)(\(A\).+?)\\section\{"
    output = list(map(lambda x: list(x),re.findall(regex,string,flags=re.DOTALL,overlapped=True)))
    output = applyLabels(output,n)
    return output 

def multiPartExtract(string,n): 
    # given string with multipart problems 
    # return list of lists of problems 
    regex = r"\\section\{Questions [0-9]{1,3}-[0-9]{1,3}\} are based on the following fact situation:(.+?)\\section\{([0-9]{1,3})\}(.+?)(\(A\).+?)\\section\{([0-9]{1,3})\}(.+?)(.+?)(\(A\).+?)\\section\{"
    lst     = list(map(list,re.findall(regex,string,flags=re.DOTALL,overlapped=True))) 
    def modify(l): 
        # input list given by multipart problem 
        # and returns list of lists containing two problems 
        l2 = [[l[1],l[0]+"\n"+l[2],l[3]],[l[4],l[0]+"\n"+l[6],l[7]]]
        return l2
    output = sum(list(map(modify,lst)),start=[])
    output = applyLabels(output,n)
    return output 


def format(problems): 
    # adjust formatting for problems list 
    problems = list(map(lambda y: list(map(lambda x: x.strip("\n") if type(x)== str else x, y)), problems))
    regex = r"\([A-D]\) "
    problems = list(map(lambda y: [y[0],y[1],list(map(lambda x: x.strip("\n"),re.split(regex,y[2],maxsplit=4,flags=re.DOTALL)))[1:]], problems))
    return problems

def answerExtract(string,n): 
    # given string with solutions
    # extract answer and match with appropriate problem 
    regex      = r"\\section\{Answer to Question ([0-9]{1,3})\}(.+?)\\section\{"
    answerKeys = list(map(lambda x: [x[0],re.search(r"\(([A-D])\)",x[1]).group(1)],re.findall(regex,string,flags=re.DOTALL,overlapped=True)))
    answerKeys = dict(applyLabels(answerKeys,n))
    return answerKeys



# return pandas and json

collabel = [
    "Problem Number", 
    "Problem Statement", 
    "Problem Choices", 
    "Final Answer", 
    "Book Title"
]

def convertPandas(string,n): 
    # given string with solutions
    # returns dataframe with matched data 
    problems = problemExtract(string,n) + multiPartExtract(string,n)
    problems = format(problems)
    answerKeys = answerExtract(string,n)
    output     = pd.DataFrame([["NAN"]*len(collabel)]*len(problems))
    val        = answerKeys.keys()
    for i in range(len(problems)): 
        if problems[i][0] in val: 
            output.iat[i,0] = problems[i][0]
            output.iat[i,1] = problems[i][1]
            output.iat[i,2] = problems[i][2]
            output.iat[i,3] = answerKeys[problems[i][0]]    
    output[4] = "Barbri" 
    output.columns = collabel
    return output

output = pd.DataFrame()

for n in range(len(sections)): 
    output = pd.concat([output,convertPandas(sections[n],n)])

output.sort_values(by=["Problem Number"])

with open("output.json", "w") as f:
    result = output.to_json(orient="records")
    parsed = json.loads(result)
    f.write(json.dumps(parsed,indent=4))


print(f"Number of problems: {len(output)}")




