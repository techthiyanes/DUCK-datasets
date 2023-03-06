# Run a given python script on all files in a given directory (not recursively!) matching a given pattern
# Usage: onall.py -d <directory> -p <extension> -s <script> --args '<arguments>'
# Give the filename of the file to be processed as the -i argument to the script

import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Run a given python script on all files in a given directory matching a given pattern')
parser.add_argument('-d', '--directory', help='Directory to search', required=True)
parser.add_argument('-e', '--extension', help='extension to match', required=True)
parser.add_argument('-s', '--script', help='Script to run', required=True)
parser.add_argument('--args', help='Arguments to pass to script', required=False, type=str, default='')
args = parser.parse_args()

# split spaces, but don't split inside double quotes
# for example, '-f "foo bar"' becomes ['-f', 'foo bar']
import shlex
args.args = shlex.split(args.args)
print(args.args)

for filename in os.listdir(args.directory):
    if filename.endswith(args.extension):
        print("Processing " + filename)
        subprocess.call(["python3", args.script, "-i", os.path.join(args.directory, filename)] + args.args)




