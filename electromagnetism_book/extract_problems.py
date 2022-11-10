import json

INPUT_FILE = "em_quals_preprocessed.txt"
OUTPUT_FILE = "output.json"

PROBLEM_NUMBERS = \
    list(range(1001, 1109)) + \
    list(range(2001, 2120)) + \
    list(range(3001, 3091)) + \
    list(range(4001, 4068)) + \
    list(range(5001, 5057))
PROBLEM_NUMBERS = list(map(str, PROBLEM_NUMBERS))

KEYWORDS = ["find", "compute", "calculate", "evaluate", "determine", "what is"]
KEYWORDS += list(map(lambda x: x.capitalize(), KEYWORDS))

BOOK = "Problems and Solutions on Electromagnetism"
TOPICS = [
    "Electrostatics",
    "Magnetostatic Field and Quasi-Stationary Electromagnetic Fields",
    "Circuit Analysis",
    "Electromagnetic Waves",
    "Relativity, Particle-Field Interactions",
]

with open(INPUT_FILE, "r") as f:
    lines = f.read()

output = json.loads("{}")

problems = lines.split("Problem:")
# remove the first element, which is empty
if not lines.startswith("Problem:"):
    problems = problems[1:]

i = 0
cnt_mcq = 0
cnt_ref = 0
total = 0
for p in problems:
    if p[0] == '[':
        num = p[1:5]
        p = p[6:]
        if PROBLEM_NUMBERS[i] != num:
            print("Problem number mismatch:", num, PROBLEM_NUMBERS[i])
            i = PROBLEM_NUMBERS.index(num)
    else:
        num = PROBLEM_NUMBERS[i]

    i += p.count("Solution:")

    if any(f"Problem {x}" in p for x in PROBLEM_NUMBERS) or \
        any(f"problem {x}" in p for x in PROBLEM_NUMBERS) or \
        any(f"Problems {x}" in p for x in PROBLEM_NUMBERS):
        print("Skipping problem", num, "because it references another problem")
        cnt_ref += 1
        continue
    if p.count("Solution:") == 0:  # a page is included twice in the pdf so there is an invalid problem here
        continue
    if p.count("Solution:") > 1:
        print("Skipping problem", num, "because there are multiple solutions")
        continue

    full_statement, full_solution = p.split("Solution:")
    topic = TOPICS[int(num[0]) - 1]

    if "The answer is" in full_solution:  # multiple choice, skip
        cnt_mcq += 1
        continue

    def extract_parts(s):
        s = s.replace(". (", ".\n(")
        s = s.replace(", (", ",\n(")

        parts = {}
        cur_key = "context"
        parts[cur_key] = ""
        for line in s.split("\n"):
            # if line starts with (a), (b)...
            if len(line) >= 3 and line[0] == '(' and line[2] == ')' and line[1].isalpha():
                cur_key = line[1]
                parts[cur_key] = ""
                line = line[3:]
            parts[cur_key] += line + "\n"
        return parts

    statement_parts = extract_parts(full_statement)
    solution_parts = extract_parts(full_solution)
    has_parts = len(statement_parts) > 1

    if statement_parts.keys() != solution_parts.keys():
        print("Skipping problem", num, "because it's hard to match parts")
        continue
    
    solution = ""
    for key in sorted(statement_parts.keys()):
        if key == "context":
            if has_parts:
                continue
            else:
                statement = full_statement
        else:
            statement = statement_parts["context"] + statement_parts[key]
        solution += solution_parts[key]

        num_with_part = num + "." + key if has_parts else num

        if not any(x in statement for x in KEYWORDS):  # ignore if not computational
            continue

        # find the last equation with an equals sign, the last term is the answer
        eqn_end = len(solution)
        while eqn_end > 0:
            eqn_end = solution.rfind("$", 0, eqn_end)
            eqn_start = solution.rfind("$", 0, eqn_end)
            if eqn_start == eqn_end - 1:
                eqn_start = solution.rfind("$", 0, eqn_start)
            if solution[eqn_start - 1] == "$":
                eqn_start -= 1
            if "=" not in solution[eqn_start:eqn_end]:
                eqn_end = eqn_start
            else:
                break
        answer_end = eqn_end if solution[eqn_end - 1] != '$' else eqn_end - 1
        answer_start = answer_end - 1
        bracket_balance = 0
        while answer_start >= 0:
            if solution[answer_start] == "}":
                bracket_balance += 1
            elif solution[answer_start] == "{":
                bracket_balance -= 1
            elif solution[answer_start] == "=" and bracket_balance == 0:
                break
            answer_start -= 1
        answer = ""
        if answer_start != -1 and answer_end != -1 and solution.find("$$", answer_start, answer_end) == -1:
            answer = solution[answer_start + 1:answer_end].strip()

            answer = answer.replace(r"\text {. }", "")
            answer = answer.replace(" .", "")
            answer = answer.replace(",", "")
            answer = answer.replace("\end{aligned}", "")
            answer = answer.replace("\end{align}", "")
            answer = answer.replace("\end{array}", "")
            answer = answer.replace("\end{gathered}", "")
            answer = answer.replace("&", "")
            answer = answer.replace(r"\\", "")
            answer = answer.strip()
            answer = "$$" + answer + "$$"

            if answer.count("left") != answer.count("right"):
                answer = ""
        if not answer:
            print("No answer found for problem", num_with_part)

        output[num_with_part] = {
            "Problem Statement": statement.lstrip(),
            "Solution": solution.lstrip(),
            "Topic": topic,
            "Book": BOOK,
            "Final Answer": answer,
        }
        total += 1


print("Problems skipped because they reference another problem:", cnt_ref)
print("MCQ (skipped):", cnt_mcq)
print("Total problems:", total)

with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=4)
