import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--book', type=str, required=True)
parser.add_argument('--topic', type=str, required=True, nargs='+', action='append')
args = parser.parse_args()

INPUT_FILE = args.input
OUTPUT_FILE = args.output

KEYWORDS = ["find", "compute", "calculate", "evaluate", "determine", "what is"]
KEYWORDS += list(map(lambda x: x.capitalize(), KEYWORDS))

BOOK = args.book

TOPICS = []
PROBLEM_NUMBERS = []
for topic in args.topic:
    assert len(topic) == 3
    TOPICS.append(topic[0])
    PROBLEM_NUMBERS += list(range(int(topic[1]), int(topic[2]) + 1))
PROBLEM_NUMBERS = list(map(str, PROBLEM_NUMBERS))

with open(INPUT_FILE, "r") as f:
    lines = f.read()

output = json.loads("{}")

problems = lines.split("Problem:")
# remove the first element, which is empty
if not lines.startswith("Problem:"):
    problems = problems[1:]

i = 0
cnt_mcq = 0
cnt_skip = 0
cnt_no_ans = 0
cnt_no_parts = 0
total = 0
for p in problems:
    if p[0] == '[':
        num = p[1:5]
        p = p[6:]
        if num not in PROBLEM_NUMBERS:
            print(num + " is not in the list of problems numbers")
        if i < len(PROBLEM_NUMBERS) and PROBLEM_NUMBERS[i] != num and num in PROBLEM_NUMBERS:
            print("Problem number mismatch:", num, PROBLEM_NUMBERS[i])
            i = PROBLEM_NUMBERS.index(num)
    else:
        if i < len(PROBLEM_NUMBERS):
            num = PROBLEM_NUMBERS[i]
        else:
            num = str(int(PROBLEM_NUMBERS[-1]) + i - len(PROBLEM_NUMBERS) + 1)

    i += p.count("Solution:")

    if any(f"Problem {x}" in p for x in PROBLEM_NUMBERS) or \
        any(f"problem {x}" in p for x in PROBLEM_NUMBERS) or \
        any(f"Problems {x}" in p for x in PROBLEM_NUMBERS):
        #print("Skipping problem", num, "because it references another problem")
        cnt_skip += 1
        continue
    if p.count("Solution:") == 0:  # a page is included twice in the pdf so there is an invalid problem here
        continue
    if p.count("Solution:") > 1:
        #print("Skipping problem", num, "because there are multiple solutions")
        cnt_skip += 1
        continue

    full_statement, full_solution = p.split("Solution:")
    topic = TOPICS[int(num[0]) - 1]

    if "The answer is" in full_solution:  # multiple choice, skip
        cnt_mcq += 1
        continue

    def extract_parts(s, is_statement):
        s = s.replace(". (", ".\n(")
        s = s.replace(", (", ",\n(")

        parts = {}
        cur_key = "context"
        parts[cur_key] = ""
        cur_text = ""
        for line in s.split("\n"):
            # if line starts with (a), (b)...
            if len(line) >= 3 and line[0] == '(' and line[2] == ')' and line[1].isalpha():
                if is_statement:
                    last_char = parts[cur_key].strip()[-1] if len(parts[cur_key].strip()) > 0 else ""
                    if last_char == ":" or last_char.isalpha():
                        parts[cur_key] += cur_text + "\n"
                        cur_text = ""
                        cur_key = line[1]
                        parts[cur_key] = line[4:] + "\n"
                    else:
                        cur_key = line[1]
                        parts[cur_key] = cur_text + "\n" + line[4:] + "\n"
                        cur_text = ""
                else:
                    cur_key = line[1]
                    parts[cur_key] = line[4:] + "\n"
            else:
                if is_statement and cur_key != "context":
                    cur_text += line + "\n"
                else:
                    parts[cur_key] += line + "\n"

        if is_statement and cur_key != "context":
            last_char = parts[cur_key].strip()[-1] if len(parts[cur_key].strip()) > 0 else ""
            if last_char == ":" or last_char.isalpha():
                parts[cur_key] += cur_text
                parts["end_context"] = ""
            else:
                parts["end_context"] = cur_text

        return parts

    statement_parts = extract_parts(full_statement, True)
    solution_parts = extract_parts(full_solution, False)
    has_parts = len(statement_parts) > 1

    statement_parts_keys = set(statement_parts.keys())
    solution_parts_keys = set(solution_parts.keys())
    statement_parts_keys.discard("context")
    statement_parts_keys.discard("end_context")
    solution_parts_keys.discard("context")
    if statement_parts_keys != solution_parts_keys:
        #print("Skipping problem", num, "because it's hard to match parts")
        cnt_skip += 1
        continue
    
    solution = solution_parts["context"] if "context" in solution_parts else ""
    for key in sorted(statement_parts.keys()):
        if key == "context":
            if has_parts:
                continue
            else:
                statement = full_statement
        elif key == "end_context":
            continue
        else:
            statement = statement_parts["context"] + statement_parts[key] + statement_parts["end_context"]
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
            answer = answer.replace("&", "")
            answer = answer.replace(r"\\", "")
            answer = answer.replace("\n", "")
            if r"\begin{aligned}"  not in answer: answer = answer.replace(r"\end{aligned}", "")
            if r"\begin{align}"    not in answer: answer = answer.replace(r"\end{align}", "")
            if r"\begin{array}"    not in answer: answer = answer.replace(r"\end{array}", "")
            if r"\begin{gathered}" not in answer: answer = answer.replace(r"\end{gathered}", "")
            if r"\begin{gather}"   not in answer: answer = answer.replace(r"\end{gather}", "")
            if r"\begin{cases}"    not in answer: answer = answer.replace(r"\end{cases}", "")
            answer = answer.strip()
            answer = "$$" + answer + "$$"

            if answer.count("left") != answer.count("right"):
                answer = ""
            if answer.count("begin") != answer.count("end"):
                answer = ""
        if not answer:
            #print("No answer found for problem", num_with_part)
            cnt_no_ans += 1

        statement = statement.strip()
        solution = solution.strip()
        # remove consecutive newlines
        while "\n\n\n" in statement:
            statement = statement.replace("\n\n\n", "\n\n")
        while "\n\n\n" in solution:
            solution = solution.replace("\n\n\n", "\n\n")

        output[num_with_part] = {
            "Problem Statement": statement,
            "Solution": solution,
            "Topic": topic,
            "Book": BOOK,
            "Final Answer": answer,
        }
        total += 1
        if not has_parts:
            cnt_no_parts += 1


print("MCQ (skipped):", cnt_mcq)
print("Skipped problems:", cnt_skip)
print("No answer found:", cnt_no_ans)
print("Problems without subparts:", cnt_no_parts)
print("Total problems:", total)

with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=4)
