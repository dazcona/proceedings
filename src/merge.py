#!/usr/bin/python

import os
import sys
from shutil import copyfile
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import subprocess
import config
from utils import read_papers_in_proceedings_order


def main():
    
    # Proceedings Front
    proceedings_front = os.path.join(config.ACM_DIR, config.PROCEEDINGS_FRONT)
    if not os.path.exists(proceedings_front):
        print('Could not find proceedings front: ' + proceedings_front)
        sys.exit(1)

    PDFS = [ proceedings_front ]
    
    # Papers directory
    if not os.path.exists(config.PAPERS_DIR):
        print('Could not find dir: ' + config.PAPERS_DIR)
        sys.exit(1)

    # Get the files in the dir
    files_in_dir = os.listdir(config.PAPERS_DIR)

    print('{0} files detected in dir {1}'.format(
        len(files_in_dir),
        config.PAPERS_DIR)
    )

    # Papers in proceedings order
    papers = read_papers_in_proceedings_order()

    count = 0
    PAPER_NUM = 1

    for paper in papers:

        # Number
        number = paper['number']
        
        # Filename
        fname = config.PAPER_FNAME.format(number)

        # Paper path
        paper_path = os.path.join(config.PAPERS_DIR, fname)
        
        if not os.path.exists(paper_path):
            print("## {0} ## Paper '{1}' not found.".format(number, paper_path))
            sys.exit(1)
        
        print("#######" * 5, number, "#######" * 5)

        # Paper's data
        authors = paper['author_names']
        first_author = authors[0]
        name = first_author.split(':')[0]
        last_name = name.split()[-1].lower()

        # ACM filename
        acm_fname = config.ACM_PAPER_FNAME.format(PAPER_NUM, last_name)

        # ACM paper path
        acm_paper_path = os.path.join(config.ACM_DIR, acm_fname)

        # Reader
        reader = PdfFileReader(paper_path)

        # Num Pages
        num_pages = reader.getNumPages()

        # Numbering
        with open(config.PROCEEDINGS_ONLY_NUMBERS_TEX, "w") as f:
            # First argument: START NUMBER
            # Second argument: NUMBER OF PAGES
            p = subprocess.run(["bash", "src/numbers.sh", str(PAPER_NUM), str(num_pages)], stdout=f)

        # Update number
        PAPER_NUM += num_pages

        # Create pages with just the numbers
        p = subprocess.run(["pdflatex",  "-halt-on-error", "-output-directory", config.PROCEEDINGS_ONLY_NUMBERS_DIR, config.PROCEEDINGS_ONLY_NUMBERS_TEX])
        print(p)

        # Create ACM paper: stamp numbers into the PDF
        p = subprocess.run(["pdftk", paper_path, "multistamp", config.PROCEEDINGS_ONLY_NUMBERS_PDF, "output", acm_paper_path])
        print(p)

        # Queueing it!
        PDFS.append(acm_paper_path)
        count += 1

    # MERGE all files
    merger = PdfFileMerger(strict=False)

    for filename in PDFS:
        print('Appending {0}'.format(filename))
        merger.append(filename)

    proceedings_file = os.path.join(config.ACM_DIR, config.PROCEEDINGS_NAME)

    # Write!
    print('Writing proceedings...')
    merger.write(proceedings_file)

    print("File '{0}' created.".format(proceedings_file))


if __name__ == '__main__':
    main()
