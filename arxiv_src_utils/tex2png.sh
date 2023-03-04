#!/bin/bash
DIRNAME=$1
cp scripts/extract.py $DIRNAME
cp scripts/clean.py $DIRNAME
cd $DIRNAME
mv *.tex main.tex
# Make folders for pdflatex output
mkdir "tex"
mkdir "png"
pdflatex --synctex=1 -interaction=nonstopmode main.tex
# Parse synctex
gzip -d *.gz
python extract.py
# Make folder for png output
pdftoppm main.pdf out -png 
# Clean up and move files
rm main.tex
mv *.tex tex
mv *.png png
python clean.py