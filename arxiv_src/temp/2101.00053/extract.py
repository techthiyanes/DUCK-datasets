import os

synctex_file, tex_file = None, None
for file_dir in os.listdir():
    if ".synctex" in file_dir:
        synctex_file = file_dir
    elif ".tex" in file_dir:
        tex_file = file_dir

with open(synctex_file, "r") as f:
    lines = f.readlines()
pages = []
for line in lines:
    if line[0] == "{":
        # Make new page start
        pages.append(int(1e9))
    else:
        comma_split = line.split(",")
        if len(comma_split) > 1:
            num = comma_split[1].split(":")[0]
            # Searching for min line number occurring in page
            pages[-1] = min(pages[-1], int(num))

with open(tex_file, "r") as f:
    lines = f.readlines()

for i, page_start in enumerate(pages):
    if i < len(pages) - 1:
        page_end = pages[i+1] - 1
    else:
        page_end = int(1e9)
    sub_text = lines[page_start - 1: page_end]
    with open("out{}.tex".format(i+1), "w") as f:
        f.writelines(sub_text)
