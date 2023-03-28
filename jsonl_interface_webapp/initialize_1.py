from flask import Flask, request, render_template, redirect
import os
import jsonlines
import requests
import subprocess

app = Flask(__name__)

cache_directory = "cache"
problems_file = "numerical.jsonl"


problems_path = os.path.join(cache_directory, problems_file)
app_path = "http://127.0.0.1:5001/"

github_root = "https://raw.githubusercontent.com/TheDuckAI/DUCK-datasets/main/final/data/"

req_to_link = {
    "math_numerical": github_root + "valid/math/numerical.jsonl",
    "math_symbolic":  github_root + "test/math/symbolic.jsonl",
    "physics_numerical": github_root + "valid/physics/physics_numerical.jsonl",
    "physics_numerical_images":  github_root + "valid/physics/physics_numerical_images.jsonl",
    "physics_symbolic": github_root + "test/physics/physics_symbolic.jsonl",
    "physics_symbolic_images":  github_root + "test/physics/physics_symbolic_images.jsonl"
}


def files_in_cache(req): 
    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)

    if not os.path.exists(problems_path) or not files_are_identical(problems_path,req_to_link[req]):
        download_file(req_to_link[req], problems_path)


 

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # for req in req_to_link:
    #     if request.args.get(req):
    #         files_in_cache(req)
    #         return redirect(app_path)
    #     else: 
    #         raise Exception("No request found")
    
    if request.args.get("math_numerical"):
        files_in_cache("math_numerical")
        return redirect(app_path)
    return render_template('index.html')


def files_are_identical(local_path, remote_url):
    response = requests.get(remote_url)
    remote_content = response.text

    with open(local_path, "r") as local_file:
        local_content = local_file.read()

    return local_content == remote_content


def download_file(url, destination):
    response = requests.get(url)
    content = response.text

    with open(destination, "w") as file:
        file.write(content)


@app.route('/template')
def template():
    # Add any necessary code to render the template.html page
    return redirect(app_path)


if __name__ == '__main__':
    app.run(port=5000,debug=False)
