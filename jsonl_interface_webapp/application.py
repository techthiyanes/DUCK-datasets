import json
import os
import requests

from flask import Flask, render_template, request, redirect

root = os.path.dirname(os.path.abspath(__file__))
counter_file = root + "/counter.txt"
current_file = root + "/current_file.txt"
cache_directory = "cache"
app_path = "http://127.0.0.1:5001/"
github_root = "https://raw.githubusercontent.com/TheDuckAI/DUCK-datasets/main/final/data/"
default_req = "math_numerical"
default_path = cache_directory + "/numerical.jsonl"

# links to the datasets
req_to_link = {
    "math_numerical": github_root + "valid/math/numerical.jsonl",
    "math_symbolic":  github_root + "test/math/symbolic.jsonl",
    "proof_like":  github_root + "test/math/proof_like.jsonl",
    #
    "physics_numerical": github_root + "valid/physics/physics_numerical.jsonl",
    "physics_numerical_images":  github_root + "valid/physics/physics_numerical_images.jsonl",
    "physics_symbolic": github_root + "test/physics/physics_symbolic.jsonl",
    "physics_symbolic_images":  github_root + "test/physics/physics_symbolic_images.jsonl",
    #
    "mcat_reading_test": github_root + "test/mcat_reading/mcat_reading_test.jsonl",
    "mcat_reading_val": github_root + "valid/mcat_reading/mcat_reading_val.jsonl",
    "mcat_science_test":  github_root + "test/mcat_science/mcat_science_test.jsonl",
    "mcat_science_val":  github_root + "valid/mcat_science/mcat_science_val.jsonl",
    "mcat_science_images_test": github_root + "test/mcat_science/mcat_science_images_test.jsonl",
    "mcat_science_images_val": github_root + "valid/mcat_science/mcat_science_images_val.jsonl",
    #
    "law": github_root + "valid/law/mcq.jsonl"
}

filename_to_req = {
    "numerical.jsonl": "math_numerical",
    "symbolic.jsonl": "math_symbolic",
    "proof_like.jsonl": "proof_like",
    #
    "physics_numerical.jsonl": "physics_numerical",
    "physics_numerical_images.jsonl": "physics_numerical_images",
    "physics_symbolic.jsonl": "physics_symbolic",
    "physics_symbolic_images.jsonl": "physics_symbolic_images",
    #

    "mcat_reading_test.jsonl": "mcat_reading_test",
    "mcat_reading_val.jsonl": "mcat_reading_val",
    "mcat_science_test.jsonl": "mcat_science_test",
    "mcat_science_val.jsonl": "mcat_science_val",
    "mcat_science_images_test.jsonl": "mcat_science_images_test",
    "mcat_science_images_val.jsonl": "mcat_science_images_val",
    #
    "mcq.jsonl": "law"
}


def download_file(url, destination):
    if not os.path.exists(destination) or not files_are_identical(destination,url):
        response = requests.get(url)
        content = response.text

        print("Downloading file...")
        with open(destination, "w") as file:
            file.write(content)


def files_in_cache(req,problems_path):
    # check if the file is in the cache
    # if it is, check if the file is up to date
    # if it is not, download the file
    download_file(req_to_link[req], problems_path)
    local_file_name = req_to_link[req].split("/")[-1]
    return os.path.join(cache_directory, local_file_name)


def read_current_file(current_file=current_file):
    # get the current file
    with open(current_file, 'r') as f:
        problems_path=f.read()
    return problems_path

def update_current_file(path,counter_file=counter_file,current_file=current_file):
    # check if the current file is the same as the one in the cache
    with open(current_file, 'r') as c:
        cf = c.read()
        if cf != path:
            cf = path
            with open(counter_file, 'w') as f:
                f.write('0')
                f.close()
            with open(current_file, 'w') as c:
                c.write(cf)
                c.close()
        c.close()

def read_current_counter(counter_file=counter_file):
    # get the current counter
    with open(counter_file, 'r') as f:
        current_index=int(f.read())
    return current_index

def update_counter(n,counter_file=counter_file):
    # update the counter
    with open(counter_file, 'w') as f:
        f.write(str(n))
        f.close()

def check_valid_path(path):
    # check if the path is valid    
    return path.endswith(".jsonl") and os.path.exists(path)

def valid_file(path): 
    # check if the file is valid jsonl
    line_count = 0
    with open(path, 'r') as file:
        for line in file:
            try:
                json.loads(line)
                line_count += 1
            except json.JSONDecodeError:
                print(f"Invalid JSON object at line {line_count + 1}")
                return False
    return True

def load_from_path(path,counter_file=counter_file,current_file=current_file):
    # load problems from path
    # check if the path is a jsonl file
    # if it is, load the problems from the file
    # if it is not, raise an error

    if check_valid_path(path):
        if not valid_file(path):
            req = path.split("/")[-1].split(".")[0]
            download_file(req_to_link[req],path)

        # generate list of json objects containing problems
        update_current_file(path)

        json_list = []
        line_count = 0
        problem_dict = dict()
        print(f"Loading problems... {path}")

        with open(path, 'r') as file:
            for line in file:
                try:
                    json.loads(line)
                    json_list.append(line)
                    line_count += 1
                except json.JSONDecodeError:
                    print(f"Invalid JSON object at line {line_count + 1}")
                    continue

        for i in range(len(json_list)):
            json_str = json_list[i]
            result = json.loads(json_str)
            problem_dict.update({i: result})
        return problem_dict
    else:
        raise ValueError("Problems file must be JSONL file")





PROBLEM_FIELDS = [
    "Topic",
    "Source",
    "Problem Statement",
    "Answer Candidates",
    "Images",
    "Solution",
    "Final Answer",
]


def list_to_str(l):
    return "\n".join(l)

def str_to_list(s):
    l = [x.strip() for x in s.split("\n")]
    l = [x for x in l if x]
    return l


app = Flask(__name__)

@app.route("/")
def index():
    current_index = read_current_counter()
    problems_path = read_current_file()

    if request.args:
        id_num = int(request.args.get('id'))
        for req in req_to_link:
            if request.args.get(req):
                problems_path = cache_directory + "/" + req_to_link[req].split("/")[-1]
                update_current_file(problems_path)
                download_file(req_to_link[req], problems_path)
                print(f"problems_path: {problems_path}")
                problem_dict = load_from_path(problems_path)
                problem = {
                    "Key": read_current_counter(),
                    "Topic": problem_dict[current_index]["Topic"] if "Topic" in problem_dict[current_index].keys() else None,
                    "Source": problem_dict[current_index]["Source"],
                    "Problem Statement": problem_dict[current_index]["Problem Statement"],
                    "Answer Candidates": problem_dict[current_index]["Answer Candidates"],
                    "Images": problem_dict[current_index]["Images"],
                    "Solution": problem_dict[current_index]["Solution"],
                    "Final Answer": problem_dict[current_index]["Final Answer"],
                }
                break
        else:
            problems_path = read_current_file()
            problem_dict = load_from_path(problems_path)
            if id_num != current_index:
                if id_num >= 0 and id_num <= len(problem_dict):
                    current_index = id_num
                else:
                    return "<p>There are no more problems!</p>"
            elif request.args.get("previous"):
                if current_index > 0:
                    current_index -= 1
                else:
                    return "<p>There are no more problems!</p>"
            elif request.args.get("next"):
                if current_index < len(problem_dict)-1:
                    current_index += 1
                else:
                    return "<p>There are no more problems!</p>"
            else:
                raise ValueError("Invalid request")
        problem = {
                "Key": read_current_counter(),
                "Topic": problem_dict[current_index]["Topic"] if "Topic" in problem_dict[current_index].keys() else None,
                "Source": problem_dict[current_index]["Source"],
                "Problem Statement": problem_dict[current_index]["Problem Statement"],
                "Answer Candidates": problem_dict[current_index]["Answer Candidates"],
                "Images": problem_dict[current_index]["Images"],
                "Solution": problem_dict[current_index]["Solution"],
                "Final Answer": problem_dict[current_index]["Final Answer"],
            }
        update_counter(current_index)
        return render_template(
                    "template.html",
                    file=read_current_file(),
                    id=read_current_counter(),
                    topic= problem["Topic"],
                    source=problem["Source"],
                    problem_statement=problem["Problem Statement"],
                    answer_candidates=list_to_str(problem["Answer Candidates"]),
                    images=list_to_str(problem["Images"]),
                    solution=problem["Solution"],
                    final_answer=problem["Final Answer"],
                    problem_dict_cnt=len(problem_dict)
                )

        # update_counter(current_index)

        # return redirect("/")

    problem_dict = load_from_path(problems_path)
    current_index = read_current_counter()


    problem = {
                "Key": read_current_counter(),
                "Topic": problem_dict[current_index]["Topic"] if "Topic" in problem_dict[current_index].keys() else None,
                "Source": problem_dict[current_index]["Source"],
                "Problem Statement": problem_dict[current_index]["Problem Statement"],
                "Answer Candidates": problem_dict[current_index]["Answer Candidates"],
                "Images": problem_dict[current_index]["Images"],
                "Solution": problem_dict[current_index]["Solution"],
                "Final Answer": problem_dict[current_index]["Final Answer"],
            }
    for field in PROBLEM_FIELDS:
        if field not in problem:
            problem[field] = ""

    print(problem)
    return render_template(
        "template.html",
        file=read_current_file(),
        id=read_current_counter(),
        topic=problem["Topic"],
        Source=problem["Source"],
        problem_statement=problem["Problem Statement"],
        answer_candidates=list_to_str(problem["Answer Candidates"]),
        images=list_to_str(problem["Images"]),
        solution=problem["Solution"],
        final_answer=problem["Final Answer"],
        problem_dict_cnt=len(problem_dict),
    )

def files_are_identical(local_path, remote_url):
    response = requests.get(remote_url)
    remote_content = response.text

    with open(local_path, "r") as local_file:
        local_content = local_file.read()

    return local_content == remote_content





@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

@app.before_request
def before_request():
    problems_path = read_current_file()
    filename = problems_path.split("/")[-1]
    # problem_dict = load_from_path(problems_path)
    # problem_keys = list(problem_dict.keys())
    files_in_cache(filename_to_req[filename],problems_path)
    pass




if __name__ == "__main__":
    app.run(port=5001,debug=True)