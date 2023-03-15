Interface for sorting numerical/symbolic problems in math/physics jsonl files.

This script is based off of [jsonl interface](https://github.com/TheDuckAI/DUCK-datasets/blob/main/jsonl_interface/README.md) and [annotation tool script](https://github.com/TheDuckAI/DUCK-datasets/tree/main/annotation_tool). 

## Usage
The script accepts the following arguments:
- `--input_file`: The path to the `.jsonl` file that contains the problems, e.g. `physics_books/data/em_quals_output.jsonl`
- `--numerical_file`: The path to the `.jsonl` file where the numerical problems without images will be stored. 
- `--numerical_images_file`: The path to the `.jsonl` file where the numerical problems with images will be stored. 
- `--symbolic_file`: The path to the `.jsonl` file where the symbolic problems without images will be stored. 
- `--symbolic_images_file`: The path to the `.jsonl` file where the symbolic problems with images will be stored. 


To run the script, use the following command:
```bash
python app.py --problems_file PATH --numerical_file PATH --numerical_images_file PATH --symbolic_file PATH --symbolic_images_file PATH 
```

You should see a message like
```bash
 * Running on http://127.0.0.1:5000
```
You can then open the link in your browser.

The file counter.txt keeps track of the line number of your current location in the input_file. 


## Note. 

The script assumes that the values for "Image" in the jsonl file are mathpix urls. 
