# split mcat questions into science and reading

import argparse
import jsonlines

def main(input_file, science_file, reading_file):
    with jsonlines.open(input_file, mode='r') as reader, \
         jsonlines.open(science_file, mode='w') as science_writer, \
         jsonlines.open(reading_file, mode='w') as reading_writer:
             
        for item in reader:
            if item.get('Topic') == 'MCAT Science':
                science_writer.write(item)
            else:
                reading_writer.write(item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split questions based on topic.')
    parser.add_argument('--input_file', type=str, required=True, help='Input jsonl file.')
    parser.add_argument('--science', type=str, required=True, help='File where the science questions will be written.')
    parser.add_argument('--reading', type=str, required=True, help='File where the reading questions will be written.')
    
    args = parser.parse_args()
    
    main(args.input_file, args.science, args.reading)
