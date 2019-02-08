#!/usr/bin/python

import os
import re
import sys
import PyPDF2
import subprocess
import config
from utils import get_paper_numbers


def walk(obj, fnt, emb):

    if not hasattr(obj, 'keys'):
        return None, None
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])

    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])

    elif '/FontName' in obj and fontkeys.intersection(set(obj)):
        emb.add(obj['/FontName'])

    for k in obj:
        if hasattr(obj[k], 'keys'):
            walk(obj[k], fnt, emb)

    return fnt, emb

def strings_in_content(str_msg_list, text):

    # initial result
    result = True
    msgs = []

    # Remove white space because the text in some pdf pages is extracted without them.

    for search_str, diag in str_msg_list:
        if search_str.replace(' ', '') not in text:
            result = False
            msgs.append(diag)

    return True, msgs


def check_pdf(paper_path):

    # Initial result to return
    result = True
    msgs = []

    # Get the text of the first page
    pdf_file = PyPDF2.PdfFileReader(paper_path, strict=False)

    # Num Pages
    num_pages = pdf_file.getNumPages()
    print('{} PAGES'.format(num_pages))

    # First page
    first_page = pdf_file.getPage(0)
    text = first_page.extractText()
    text_nsp = text.replace(' ', '').replace('\n', '')
    # print(text_nsp)

    # doc_info = pdf_file.getDocumentInfo()
    # print(doc_info)

    if text_nsp == '': # PDF is BLANK

        result = False
        msgs = ['BLANK! Text could not be extracted, please check manually!']

    else:

        # Check content in the first page
        result, msgs = strings_in_content(
            [('CCS CONCEPTS', 'No CCS CONCEPTS section detected'),
            ('KEYWORDS', 'No KEYWORDS section detected'),
            ('ACM Reference Format', 'No ACM Reference Format section detected'),
            ('ABSTRACT', 'No ABSTRACT section detected'),
            ],
            text_nsp
        )

        # Detect text in the copyright
        c1, _ = strings_in_content([('Copyright is held by','')], text_nsp)
        c2, _ = strings_in_content([('Copyright held by','')], text_nsp)
        c3, _ = strings_in_content([('This article was authored by employees','')],
                                text_nsp)
        if not c1 and not c2 and not c3:
            result = False
            msgs.append('No Copyright section detected')

        # Detect DOI
        matches = re.findall(config.DOI, text_nsp)
        if len(matches) != 2:
            result = False
            msgs.append('DOI not detected twice in first page ({0})'.format(len(matches)))

        # Detect Venue
        matches = re.findall(config.VENUE.replace(' ', ''), text_nsp, re.MULTILINE)
        if len(matches) != 2:
            result = False
            msgs.append(
                'Venue not detected twice in first page ({0})'.format(len(matches))
            )

        # Detect number pages
        pages_str = '{0} pages.'.format(num_pages)
        matches = re.findall(pages_str.replace(' ', ''), text_nsp)
        if len(matches) != 1:
            result = False
            msgs.append('Pages not detected in first page')

    # Embedded fonts
    fonts = set()
    embedded = set()
    for page in pdf_file.pages:
        obj = page.getObject()
        f, e = walk(obj['/Resources'], fonts, embedded)
        fonts = fonts.union(f)
        embedded = embedded.union(e)

    unembedded = fonts - embedded
    if unembedded:
        result = False
        msgs.append('Unembedded Fonts: ' + str(unembedded))

    return result, msgs


def main():

    # Papers directory
    if not os.path.exists(config.PAPERS_DIR):
        print('Could not find dir ' + config.PAPERS_DIR)
        sys.exit(1)

    # Get the files in the dir
    files_in_dir = os.listdir(config.PAPERS_DIR)

    print('{0} files detected in dir {1}'.format(
        len(files_in_dir),
        config.PAPERS_DIR)
    )

    # Paper numbers
    paper_numbers = get_paper_numbers()

    count = 0
    papers_with_issues = []

    for number in paper_numbers:
        
        # Filename
        fname = config.PAPER_FNAME.format(number)

        # Paper path
        paper_path = os.path.join(config.PAPERS_DIR, fname)
        
        if not os.path.exists(paper_path):
            print("## {0} ## Paper '{1}' not found.".format(number, paper_path))
            sys.exit(1)
        
        print("## {0} ## Analysing Paper {1}:".format(number, paper_path))

        # PDF TESTS
        
        # PDF test using bash, pdftotext and pdffonts
        p = subprocess.run(["bash", "src/check.sh", paper_path])
        bash_result = p.returncode == 0

        # PDF test using python and PyPDF2
        py_result, msgs = check_pdf(paper_path)

        if not bash_result and not py_result: # BOTH have to fail
            print('Paper {0} has issues:'.format(number))
            print('  ' + '\n  '.join(msgs))
            papers_with_issues.append(number)
        else:
            print('Paper {0} is OK.'.format(number))

    print('#' * 100)
    print('{0} papers have issues out of {1}:'.format(len(papers_with_issues), len(paper_numbers)))
    print(', '.join(papers_with_issues))
    print('#' * 100)


if __name__ == '__main__':
    main()
