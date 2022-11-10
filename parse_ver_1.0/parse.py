import os  
import pandas as pd
import re 
# also requires pdflatex on machine


file = "berkeley_output.json" # input("INPUT: Json file?")
js = open(file, "r").read()
df = pd.read_json(js)
col = df.columns
row = df.index


preamble = "\\documentclass[10pt]{article}\n\\usepackage{hyperref}\n\\usepackage{amsthm}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n\\usepackage{amsfonts}\n\\setlength\\parindent{0pt}\n\\title{OUTPUT.TEX.}\n\\date{Updated: \\today}\n\\author{}\n\n\n\\begin{document}"



output = preamble


    
for c in col:
    output += "\n\n"
    for i in range(1,len(row)):
        output += "\n" + r"\textbf{" + row[i] + r"} :"
        s = str(df[c][i])
        output += s
        output += r"\\"
    if s and "\n" in s[-3:]: #s[-1].isspace()
        output += r"\vspace{2em}" + "\n"
output += "\\end{document}"
        


output = re.subn(r"\!\[\]\(https\:\/\/cdn\.mathpix\.com\/cropped\/[0-9a-zA-Z=&_?\.-]+\)","MATHPIX IMAGE",output)[0]
output = re.subn(r"\n\n\\\\","",output)[0]
output = re.subn(r"(\\section\{\([a-zA-Z\.\s]+\)\})\n\\","\\1",output)[0]
output = re.subn("ु","",output)[0]
output = re.subn(r"(S_{n}, A_{n}, D_{n})",r"$\1$",output)[0]

with open('output.tex', 'w') as f:
    f.write(output)    
 







os.system("pdflatex output.tex")
