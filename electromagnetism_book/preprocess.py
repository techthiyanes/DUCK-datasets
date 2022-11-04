INPUT_FILE = "em_quals.txt"
OUTPUT_FILE = "em_quals_preprocessed.txt"

PROBLEM_NUMBERS = \
    list(range(1001, 1109)) + \
    list(range(2001, 2120)) + \
    list(range(3001, 3091)) + \
    list(range(4001, 4068)) + \
    list(range(5001, 5057))
PROBLEM_NUMBERS = list(map(str, PROBLEM_NUMBERS))

with open(INPUT_FILE, "r") as f:
    lines = f.readlines()
    # remove "\n" from each line
    lines = [line[:-1] for line in lines]

# keep only lines between "\section{BASIC LAWS OF ELECTROSTATICS (1001-1023)}\n" and "\section{INDEX TO PROBLEMS}\n"
lines = lines[lines.index("\section{BASIC LAWS OF ELECTROSTATICS (1001-1023)}") + 1:lines.index("\section{INDEX TO PROBLEMS}")]

# replace "\section{Solution:}" with "Solution:"
lines = [line.replace(r"\section{Solution:}", "Solution:") for line in lines]

# remove all "\section{...}" that contain only uppercase letters -- those correspond to headings
lines = [line for line in lines if not (line.startswith(r'\section{') and line[8:].isupper())]

# if a "\section{...}" contains only a number, replace the whole line with "Problem:"
lines = [line if not (line.startswith(r"\section{") and line[9].isdigit()) else "Problem:" for line in lines]

# remove all other section environments
assert sum(line.startswith(r"\section{") for line in lines) == sum(line.find(r"\section{") != -1 for line in lines)
assert all(line.endswith("}") for line in lines if line.startswith(r"\section{"))
lines = [line if not line.startswith(r"\section{") else line[9:-1] for line in lines]

# remove all problem sources
lines = "\n".join(lines)
lines = lines.replace("(Wisconsin)", "")
lines = lines.replace("(UC, Berkeley)", "")
lines = lines.replace("(Columbia)", "")
lines = lines.replace("(Princeton)", "")
lines = lines.replace("(Chicago)", "")
lines = lines.replace("(CUSPEA)", "")
lines = lines.replace("$(S U N Y$, Buffalo)", "")
lines = lines.replace("$(M I T)$", "")
lines = lines.replace("$(\operatorname{MIT})$", "")
lines = lines.replace("$(C C T)$", "")
lines = lines.replace("(Coulumbia)", "")
lines = lines.replace("$(U C$, Berkeley)", "")
lines = lines.replace("(SUNY, Buffalo)", "")
lines = lines.replace("$(S U N Y, B u f f a l o)$", "")
lines = lines.split("\n")

# count lines that start with "![](https://cdn.mathpix.com"
print("Number of image links:", len([line for line in lines if line.startswith("![](https://cdn.mathpix.com")]))

# sometimes the problem number is in $$ ... $$, so we need to fix that
lines = "\n".join(lines)
for x in PROBLEM_NUMBERS:
    lines = lines.replace(f"$$\n{x}\n$$\n", f"{x}\n")
lines = lines.split("\n")

# remove "\begin{abstract}" and "\end{abstract}"
lines = [line for line in lines if not line.startswith(r"\begin{abstract}") and not line.startswith(r"\end{abstract}")]

# manual fixes
lines = "\n".join(lines)
lines = lines.replace("$$\n\\begin{gathered}\n1001 \\\\", "1001\n$$\n\\begin{gathered}")
lines = lines.replace(r"\section{Solution: \\ Solution:}", "Solution:")
lines = lines.split("\n")

# replace all occurrences of a problem number with "Problem (number):"
new_lines = []
for line in lines:
    if  not any(x in line for x in PROBLEM_NUMBERS) or \
        line.startswith("![](https://cdn.mathpix.com") or \
        any(f"Problem {x}" in line for x in PROBLEM_NUMBERS) or \
        any(f"problem {x}" in line for x in PROBLEM_NUMBERS) or \
        any(f"Problems {x}" in line for x in PROBLEM_NUMBERS):
        new_lines.append(line)
        continue
    assert(line[-4:] in PROBLEM_NUMBERS)
    new_lines.append(line[:-4])
    new_lines.append(f"Problem:[{line[-4:]}]")
lines = new_lines

print("Number of solutions:", len([line for line in lines if line.startswith("Solution:")]))
print("Number of problems without number:", len([line for line in lines if line == "Problem:"]))
print("Number of problems with number:", len([line for line in lines if line.startswith("Problem:[")]))
print("Total number of problems:", len([line for line in lines if line.startswith("Problem:")]))

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))

# remove empty lines
#lines = [line for line in lines if line != ""]

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))