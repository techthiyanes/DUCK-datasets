from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import os
import jsonlines
import requests
import subprocess

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secret key for your app
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

cache_directory = "cache"
app_path = "http://127.0.0.1:5001/"
github_root = "https://raw.githubusercontent.com/TheDuckAI/DUCK-datasets/main/final/data/"
problems_path = cache_directory + "/numerical.jsonl"

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
    "mcat_reading_test": github_root + "test/mcat/mcat_reading_test.jsonl",
    "mcat_reading_val": github_root + "valid/mcat/mcat_reading_val.jsonl",
    "mcat_science_test":  github_root + "test/mcat/mcat_science_test.jsonl",
    "mcat_science_val":  github_root + "valid/mcat/mcat_science_val.jsonl",
    "mcat_science_images_test": github_root + "test/mcat/mcat_science_images_test.jsonl",
    "mcat_science_images_val": github_root + "valid/mcat/mcat_science_images_val.jsonl",
    #
    "law": github_root + "valid/law/mcq.jsonl"
}



def files_in_cache(req): 
    local_file_name = req_to_link[req].split("/")[-1]
    problems_path = os.path.join(cache_directory, local_file_name)
    session['problems_path'] = problems_path
    if not os.path.exists(problems_path) or not files_are_identical(problems_path,req_to_link[req]):
        download_file(req_to_link[req], problems_path)



@app.route('/', methods=['GET', 'POST'])
def index():
    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)

    for req in req_to_link:
        if request.args.get(req): 
            files_in_cache(req)
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
    app.run(port=5000,debug=True)
