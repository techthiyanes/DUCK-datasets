import json 
import re


# INPUT_FILE = 'json/mechanics_quals_output_final.json'

def preprocess_json(input_file_path):
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    result = []
    for problem_num, problem_info in data.items():
        problem_info['Problem Number'] = problem_num
        problem_info['Source'] = problem_info.pop('Book')
        problem_info['Answer candidates'] = []
        problem_info['Images'] = []
        result.append(problem_info)
    return json.dumps(result)

def bad_questions(entry):
    problem_statement = entry.get('Problem Statement', '')
    final_answer = entry.get('Final Answer', '')
    if '\\begin{tabular}' in problem_statement:
        return True
    if len(problem_statement) < 20:
        return True
    if not final_answer:
        return True
    return False

def formatting(problem_number, problem_info):
    problem_statement = problem_info.get('Problem Statement', '')
    answer_candidates = problem_info.get('Answer candidates', [])
    solution = problem_info.get('Solution', '')
    images = problem_info.get('Images', [])
    
    # Remove mathpix hyperlink and append to Images
    problem_statement = re.sub(r'!\[\]\(https://cdn.mathpix.com/[^)]+\)', '', problem_statement)
    answer_candidates = [re.sub(r'!\[\]\(https://cdn.mathpix.com/[^)]+\)', '', candidate) for candidate in answer_candidates]
    solution = re.sub(r'!\[\]\(https://cdn.mathpix.com/[^)]+\)', '', solution)
    images.extend(re.findall(r'https://cdn.mathpix.com/[^)]+', problem_statement + ' ' + ' '.join(answer_candidates) + ' ' + solution))
    
    # Replace any new line character "\n" repeated more than three consecutive times with just "\n\n"
    problem_statement = re.sub(r'\n{3,}', '\n\n', problem_statement)
    answer_candidates = [re.sub(r'\n{3,}', '\n\n', candidate) for candidate in answer_candidates]
    solution = re.sub(r'\n{3,}', '\n\n', solution)
    
    problem_info['Source'] = problem_info['Book']
    del problem_info['Book']
    problem_info['Problem Number']    = problem_number
    problem_info['Problem Statement'] = problem_statement
    problem_info['Answer Candidates'] = answer_candidates
    problem_info['Solution'] = solution
    problem_info['Images'] = images
    
    return problem_info

def process_json_file(input_file):
    with open(input_file, 'r') as file:
        input_jsonl = file.read()
        data = json.loads(input_jsonl)
    result = []
    key_order = {
        "Problem Number": 0, 
        "Topic": 1, 
        "Source": 2, 
        "Problem Statement": 3, 
        "Answer Candidates": 4, 
        "Solution": 5, 
        "Final Answer": 6, 
        "Images": 7
    }
    for i in data:
        problem_info = data[i]
        if not bad_questions(problem_info):
            formatted_info = formatting(i,problem_info)
            formatted_info = dict(sorted(formatted_info.items(), key=lambda item: key_order.get(item[0], float('inf'))))
            result.append(json.dumps(formatted_info))
    return '\n'.join(result)





FILE_LIST = [
    "json/mechanics_quals_output_final.json",
    "json/solid_state_output.json",
    "json/em_quals_output_final.json",        
    "json/optics_output_final.json",          
    "json/quantum_output_final.json",         
    "json/statmech_output.json"
]

for INPUT_FILE in FILE_LIST: 
    OUTPUT_FILE = "output/" + INPUT_FILE[5:-5] + ".jsonl"
    result = process_json_file(INPUT_FILE)

    # Other errors 

    # Replace the matched pattern with \\frac{(single digit integer)}{(single digit integer)}
    pattern = r'\\frac(\d)(\d)'
    result= re.sub(pattern, r'\\frac{\1}{\2}', result)

    f = open(OUTPUT_FILE, "a")
    f.truncate(0)
    f.write(result)