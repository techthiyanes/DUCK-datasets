## Requirements
You need to install `flask`.
```bash
pip install flask
```

## Usage
The script accepts the following arguments:
- `--problems_file`: The path to the `.json` file that contains the problems, e.g. `physics_books/data/em_quals_output.json`.
- `--final_problems_file` (optional): The path to the `.json` file where the final problems will be saved. If not provided, filename will be `problems_file` with `_final` appended, e.g. `physics_books/data/em_quals_output_final.json`.
- `--rejected_problems_file` (optional): The path to the `.json` file where the rejected problems will be saved. If not provided, filename will be `problems_file` with `_rejected` appended, e.g. `physics_books/data/em_quals_output_rejected.json`.
- `--show_images` (optional): If provided, the field "Images" will be shown. Otherwise, it will be hidden.
- `--show_choices` (optional): If provided, the field "Problem Choices" will be shown. Otherwise, it will be hidden.

To run the script, use the following command:
```bash
python app.py --problems_file FILE
```
Add the `--show_images` and/or `--show_choices` flags if you're dealing with problems that have images and/or multiple choice problems.

You should see a message like
```bash
 * Running on http://127.0.0.1:5000
```
You can then open the link in your browser and should see something like this:
![Screenshot](screenshot.png)

You can edit the problem fields, and the displays below should update accordingly.
A doc with instructions can be found on Discord.

Entries in fields that are supposed to be lists, i.e. "Problem Choices" and "Images", should each be on a separate line.

When you're done, click the "Accept" button to save the problem. If the problem is not suitable (e.g. it's not a computational problem, see the instructions doc), click "Reject". If you're not sure for now, or you want to come back to it later, click "Skip".
After that the next problem will be loaded.

Final problems will be saved to `final_problems_file`, and rejected problems will be saved to `rejected_problems_file`, while the original `problems_file` will not be modified.

> **Note**
> 
> Your progress is saved every time you click "Accept" or "Reject", so you can stop the script at any time and resume later. Note that if you edit and skip a problem, your changes will be lost when you stop the script.
> 
> To resume, simply run the script again with the same arguments.

When you re-run the script, please close the old browser tab and open a new one. Also, please don't edit the problem files while the script is running.

## Notes
The script uses ![KaTeX](https://katex.org/) to render LaTeX. While it supports most LaTeX commands, it doesn't support all of them. If you encounter a valid LaTeX formula that KaTeX doesn't render, you can edit it or probably just leave it as is.

The script assumes that the problems `.json` is a dictionary where the keys are the problem IDs and the values are the problem data. The problem data is a dictionary with the following keys:

- Topic
- Book
- Problem Statement
- Problem Choices (for multiple choice problems)
- Images (if there are any)
- Solution
- Final Answer

"Problem Choices" and "Images" are lists of strings, while the rest are strings.