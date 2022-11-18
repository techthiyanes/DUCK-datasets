README 


1. MATHPIX CONVERSION ERRORS. If there are any conversion errors (e.g. Mathpix incorrectly converted $12,000 to $\$ 12,000$), use the `regexes_clean` variable to eliminate it. `regexes_clean` is a list of lists of length 2 where the first element is the regex capturing the conversion errors and the second element specifies how the error should be converted. For instance, the above example can be corrected using [r"\$\\\$",r"\$"]

2. FILES. See assets folder for files produced in intermediate steps. modified.txt is the original txt file after conversion errors have been eliminated using regexes_clean. sections_i.txt (for 0<=i<=8) contain problems and solutions for the respective sections. 

3. KNOWN BUG. As of version 2.0, this script produces 667 problems (≈ 94.5%) Around 40 problems are lost due to the fact that problemExtract, multiPartExtract, and answerExtract fail to scrape some of the problems from the document. (Try printing len(answerKeys) and len(problems) in convertPandas.)




Number of problems in Barbri document: 

Workshop Testing Drills 102
Constitutional Law 17
Contracts 17
Criminal Law 17
Evidence 17
Real Property 17
Torts 17

Mixed Subject Questions 200
Questions 200

Multistate Practice Exam 200
AM Exam 100
PM Exam 100

Released Multistate Questions 204
Constitutional Law 34
Contracts 34
Criminal Law 34
Evidence 34
Real Property 34
Torts 34

TOTAL: 706 (≈ 2100/3)

