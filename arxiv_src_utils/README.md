# Script Usage

The script expects a path to ArXiv data downloaded directly from the ArXiv S3 dump. Four step of processing are then run:

1. Untarring of each tar file containing 500 ArXiv papers. Files are extract to `output_dir`.
2. gzip extraction of each untarred paper. Each gzipped file is deleted once it has been unzipped.
3. Alignment of each paper's tex file to the corresponding pdf page
4. Postprocessing to remove unsuccessfully compiled files.

Run using `python run.py --arxiv_src $PATH_TO_ARXIV_S3_DUMP --output_dir $PATH_TO_OUTPUT_DIR --num_workers $NUM_CPU_CORES`