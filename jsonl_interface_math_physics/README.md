Interface for sorting jsonl files containing math and physics problems. 

This script is based off of [jsonl_interface](https://github.com/TheDuckAI/DUCK-datasets/tree/main/jsonl_interface) and [annotation tool script](https://github.com/TheDuckAI/DUCK-datasets/tree/main/annotation_tool). 

## Requirements

See requirements.txt. 

## Usage
The script accepts the following arguments:
- `--problems_file`: The path to the `.jsonl` file that contains the problems, e.g. `physics_books/data/em_quals_output.jsonl`.


To run the script, use the following command:
```bash
python app.py --problems_file PATH_TO_FILE
```

You should see a message like
```bash
 * Running on http://127.0.0.1:5000
```
You can then open the link in your browser. 

## Warning. 

Please make sure to keep backup of your jsonl files. *If you open a new jsonl file from the one you are working on, your old jsonl files will be deleted.*

## Note. 

The script assumes that the values for "Image" in the jsonl file are mathpix urls. 
