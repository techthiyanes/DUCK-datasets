import json

integer_list = [3,14,19,21,26,31,53,54]
float_list = [4]
fraction_list = [5,37,38,45,47,49,51,52,58]
exact_list = [1,9,17,20,24,25,29,32,46,55]
exact_string_list = """EXACT. Write the answer as $\frac{a}{\pi^2}$, in reduced form, for integer a.
EXACT. Write the answer as $\frac{a}{b}+\frac{c}{d} \log f$, in reduced form, for integers a,b,c,d,f.
EXACT. Write the answer as $2^a$, for integer a.
EXACT. Write the answer as $ \arctan \frac{a}{\pi}-\frac{\pi}{b} $, in reduced form, for integers a,b
EXACT. Write the answer as $\frac{\pi}{a \sqrt{2}} \ln \frac{\sqrt{b}+c}{\sqrt{d}-f}  $, in reduced form, for integers a,b,c,d,f.
EXACT. Write the answer as $ \frac{\pi}{a} \ln b$, in reduced form, for integers a,b.
EXACT. Write the answer as $\frac{\pi}{a}$, for integer a.
EXACT. Write the answer as $-a^{b}$, for integers a, b.
EXACT. Write the answer as $\frac{\pi}{a}$, for integer a.
EXACT. Write the answer as $ \frac{a}{b}(a \sqrt{d}-f) $, in reduced form, for integers a,b,c,d,f.""".split('\n')

with open("putnam_numerical.jsonl", "w") as output_file:
    with open("putnam.jsonl",'r') as file:
        file = file.read()
        data = [json.loads(line) for line in file.split("\n")]
        for c,line in enumerate(data):
            if c in integer_list:
                line["Output Format Instructions"] = "INTEGER"
            if c in float_list:
                line["Output Format Instructions"] = "FLOAT"
            if c in fraction_list:
                line["Output Format Instructions"] = "EXACT. Write the answer as $\frac{a}{b}$, in reduced form, for a,b integers."
            if c in exact_list:
                line["Output Format Instructions"] = exact_string_list[exact_list.index(c)]
            if c in integer_list or c in float_list or c in fraction_list or c in exact_list:
                output_file.write("\n"+json.dumps(line))