Interface for viewing JSONL files from dataset.

This script is based off of the [annotation tool script](https://github.com/TheDuckAI/DUCK-datasets/tree/main/annotation_tool) by pvidas. 

## Requirements
You need to install `flask`.
```bash
pip install flask
```

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

## Note. 

The script assumes that the values for "Image" in the jsonl file are mathpix urls. 
