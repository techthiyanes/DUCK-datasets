Interface for sorting numerical/symbolic problems in math/physics jsonl files.

This script is based off of [jsonl interface](https://github.com/TheDuckAI/DUCK-datasets/blob/main/jsonl_interface/README.md) and [annotation tool script](https://github.com/TheDuckAI/DUCK-datasets/tree/main/annotation_tool). 

## Usage
The script accepts the following arguments:
- `--input_file`: The path to the `.jsonl` file that contains the problems
- `--output_file`: The path to the `.jsonl` file where outputs are stored.


To run the script, use the following command:
```bash
python3 app.py --input_file PATH --output_file PATH 
```

You should see a message like
```bash
 * Running on http://127.0.0.1:5000
```
You can then open the link in your browser.

The file counter.txt keeps track of the line number of your current location in the input_file. 


## Note. 

- The script assumes that the values for "Image" in the jsonl file are mathpix urls. 
- When working on a new jsonl file, change counter.txt to "0"
