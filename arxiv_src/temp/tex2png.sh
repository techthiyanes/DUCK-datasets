#!/bin/bash
#FILENAME=$(echo $1 | cut -d'.tex' -f 1)
FILENAME=$1
rm -r $FILENAME
mkdir $FILENAME
cp $FILENAME.tex $FILENAME
cp extract.py $FILENAME
cd $FILENAME
mv *.tex $FILENAME.tex
# Make folder for pdflatex output
mkdir "tex"
cp *.tex "tex"
cp extract.py "tex"
cd "tex"
pdflatex --synctex=1 *.tex
# Parse synctex
gzip -d *.gz
python extract.py
rm .py
cd ..
# Make folder for png output
mkdir "png"
mv tex/*.pdf "png"
rm tex/$FILENAME*
cd "png"
pdftoppm *.pdf out -png
rm *.pdf
cd ..
# Clean up extra files
rm $FILENAME.tex
rm *.py
cd ..
