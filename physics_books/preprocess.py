import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

INPUT_FILE = args.input
OUTPUT_FILE = args.output

PROBLEM_NUMBERS = list(map(str, range(1001, 8000)))

with open(INPUT_FILE, "r") as f:
    lines = f.readlines()
    # remove "\n" from each line
    lines = [line[:-1] for line in lines]

# keep only lines after "\section{CONTENTS}"
lines = lines[lines.index("\section{CONTENTS}") + 1:]
# keep only lines after the first uppercase section
lines = lines[min(i for i, line in enumerate(lines) if (line.startswith(r'\section{') and line[8:].isupper())):]
# keep only lines before "\section{INDEX TO PROBLEMS}" or "\section{Index to Problems}"
if "\section{INDEX TO PROBLEMS}" in lines:
    lines = lines[:lines.index("\section{INDEX TO PROBLEMS}")]
if "\section{Index to Problems}" in lines:
    lines = lines[:lines.index("\section{Index to Problems}")]

# replace "\section{Solution:}" with "Solution:"
lines = [line.replace(r"\section{Solution:}", "Solution:") for line in lines]
lines = [line.replace(r"\section{Solution}", "Solution:") for line in lines]
lines = [line.replace(r"\section{Solution: \\ Solution:}", "Solution:") for line in lines]

# remove all "\section{...}" that contain only uppercase letters -- those correspond to headings
lines = [line for line in lines if not (line.startswith(r'\section{') and line[8:].isupper())]

# if a "\section{...}" contains only a number, replace the whole line with "Problem:"
lines = [line if not (line.startswith(r"\section{") and line[9].isdigit()) else "Problem:" for line in lines]

# remove all other section environments
assert sum(line.startswith(r"\section{") for line in lines) == sum(line.find(r"\section{") != -1 for line in lines)  # max one section per line
#assert all(line.endswith("}") for line in lines if line.startswith(r"\section{"))
lines = [line[9:-1] if line.startswith(r"\section{") and line.endswith("}") else line for line in lines]
lines = [line[9:] if line.startswith(r"\section{") else line for line in lines]
# same for subsections
lines = [line[12:-1] if line.startswith(r"\subsection{") and line.endswith("}") else line for line in lines]

# remove all "\title{...}" and "\author{...}" environments
for i in range(len(lines)):
    if lines[i].startswith(r"\title{") or lines[i].startswith(r"\author{"):
        assert lines[i + 2].startswith("}")
        lines[i] = ""
        lines[i + 2] = ""

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
lines = lines.replace("$(W$ isconsin)", "")
lines = lines.replace("$(U C$, Berkeley $)$", "")
lines = lines.replace("(Princeton $)$", "")
lines = lines.replace("$(C U S P E A)$", "")
lines = lines.replace("$(U C, B$ Berkeley $)$", "")
lines = lines.replace("$(U C$, Berkele $y)$", "")
lines = lines.replace("(Wisconsin )", "")
lines = lines.replace("(Buffalo)", "")
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
if "optics" in INPUT_FILE:
    lines = lines.replace("1084", "1034")
    lines = lines.replace("2081", "2031")
    lines = lines.replace("2083", "2033")
    lines = lines.replace("A glass cube", "Problem:\n\nA glass cube")
    lines = lines.replace("A rainbow", "Problem:\n\nA rainbow")
lines = lines.replace("Solutlon", "Solution")
lines = lines.replace("Solntion", "Solution")
lines = lines.replace("Alternative Solution:", "Alternative solution:")  # hack so that it's not confused with "Solution:"
lines = lines.replace("〉", ">")
lines = lines.replace("〈", "<")
lines = lines.replace("ẹ", "e")
lines = lines.replace("Fis.", "Fig.")
lines = lines.replace("Pig.", "Fig.")
lines = lines.split("\n")

# split every "Solution:" into a separate line
lines = "\n".join(lines)
lines = lines.replace("Solution: ", "Solution:\n")
lines = lines.replace(" Solution:", "\nSolution:")
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
    #assert line[-4:] in PROBLEM_NUMBERS, line
    if not line[-4:] in PROBLEM_NUMBERS:
        new_lines.append(line)
        continue
    new_lines.append(line[:-4])
    new_lines.append(f"Problem:[{line[-4:]}]")
lines = new_lines

print("Number of solutions:", len([line for line in lines if line.startswith("Solution:")]))
print("Number of problems without number:", len([line for line in lines if line == "Problem:"]))
print("Number of problems with number:", len([line for line in lines if line.startswith("Problem:[")]))
print("Total number of problems:", len([line for line in lines if line.startswith("Problem:")]))

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))