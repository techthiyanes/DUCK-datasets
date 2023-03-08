import json


def load_jsonl(file_name):
    lines = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            lines.append(json.loads(line))
    return lines



def save_jsonl(dicts, file_name):
    with open(file_name, "w") as f:
        for d in dicts:
            json.dump(d, f)
            f.write("\n")


def save_results(dicts, save_dir):
    """
    Utility for saving evaluation results. Expects a master dict with 
    subject names indexing into a list holding questions and results for all questions in a subject.
    """
    for subject, d in dicts.items():
        save_jsonl(d, os.path.join(save_dir, "{}.jsonl".format(subject)))