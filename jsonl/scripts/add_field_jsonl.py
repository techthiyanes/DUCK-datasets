# Script that adds a field to a jsonl file
# Usage: python3 add_field_jsonl.py -i <input_file> -o <output_file> -f <field_name> -v <field_value>
# If the output file is not specified, the input file is overwritten

import sys
import json
import argparse

keys_order = [
    "Problem Number", "Topic", "Source", "Problem Statement", "Answer Candidates", 
    "Output Format Instructions", "Solution", "Final Answer", "Images", 
]

parser = argparse.ArgumentParser(description='Add a field to a jsonl file')
parser.add_argument('-i', '--input', help='Input file', required=True)
parser.add_argument('-o', '--output', help='Output file', required=False)
parser.add_argument('-f', '--field', help='Field name', required=True)
parser.add_argument('-v', '--value', help='Field value', required=False, default='')

args = parser.parse_args()
if args.output is None:
    args.output = args.input

lines = []
with open(args.input, 'r') as input_file:
    for line in input_file:
        line = line.strip()
        if line:
            json_obj = json.loads(line)
            json_obj[args.field] = args.value
            # Reorder keys
            json_obj = {k: json_obj.get(k) for k in keys_order}
            lines.append(json.dumps(json_obj))

with open(args.output, 'w') as output_file:
    for line in lines:
        output_file.write(line + '\n')
        
                
# End of script

    
