import json
import random

reading = {}
science = {}
with open('output.json') as file:
    data = json.load(file)
    for i in range(672):
        i = str(i)
        if data[i]["Topic"] == "MCAT Reading":
            reading[data[i]["Problem Number"]] = data[i]
        else:
            science[data[i]["Problem Number"]] = data[i]


sample = {**dict(random.sample(science.items(), 200)), **reading}

with open('output_sampled.json', 'w') as f:
    json.dump(sample, f)
