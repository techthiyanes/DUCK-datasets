import os

synctex_file = "main.synctex"
tex_file = "main.tex"

with open(synctex_file, "r") as f:
    lines = f.readlines()
pages = []
back = 0
for i, line in enumerate(lines):
    if line[0] == "{":
        # Make new page start
        back = pages[-1] if len(pages) > 0 else 0
        pages.append(int(1e9))
    else:
        comma_split = line.split(",")
        if len(comma_split) > 1:
            num = comma_split[1].split(":")[0]
            # Searching for min line number occurring in page
            #pages[-1] = min(pages[-1], max(int(num), back))
            if int(num) > back:
                pages[-1] = min(pages[-1], int(num))
    

#print(pages)

with open(tex_file, "r") as f:
    lines = f.readlines()

def convert(i, n):
    extra_zeros = ["0"]*(len(str(n))-len(str(i)))
    return "".join(extra_zeros) + str(i)

for i, page_start in enumerate(pages):
    if i < len(pages) - 1:
        page_end = pages[i+1] - 1
    else:
        page_end = int(1e9)
    sub_text = lines[page_start - 1: page_end]
    #print(page_start, page_end)
    #print(sub_text)
    with open("out-{}.tex".format(convert(i+1, len(pages))), "w") as f:
        f.writelines(sub_text)