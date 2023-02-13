import json
import random
import jsonlines

reading = {}
science = {}
with open('output.json') as file:
    data = json.load(file)
    for i in range(660):
        i = str(i)
        if data[i]["Topic"] == "MCAT Reading":
            reading[data[i]["Problem Number"]] = data[i]
        else:
            if data[i]["Final Answer"] != "":
                science[data[i]["Problem Number"]] = data[i]


sample = {**dict(random.sample(science.items(), 200)), **reading}

sample = sample.values()

# with open('output_sampled.json', 'w') as f:
#     json.dump(sample, f)


with jsonlines.open('output_sampled.jsonl', 'w') as writer:
    writer.write_all(sample)