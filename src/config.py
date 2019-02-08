#!/usr/bin/python

import os
import private

# A configuration file

GOOGLE_API_KEY = private.GOOGLE_API_KEY
GOOGLE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"

CONFERENCE_ID = 'AICPS-01933'
CONFERENCE = 'The 9th International Learning Analytics and Knowledge Conference (LAK 2019)'
CONFERENCE_CODE = 'LAK19'
WEBSITE = 'https://lak19.solaresearch.org/'
LOCATION = 'Tempe, AZ, USA'
TIME = 'March 4-8, 2019'
ISBN = '978-1-4503-6256-6'

DOI = 'https://doi.org/[\s\n]*10.1145/[\s\n]*3303772.[\s\n]*330'
VENUE = 'March[4.+8,]?2019, Tempe,[\s\n]*AZ, USA'

PAPERS_CSV = 'papers.csv' # 'papers_sample.csv'
ACM_CSV = 'acm.csv' # 'acm_sample.csv'
SCHEDULE_TXT = 'schedule.txt'

PAPERS_DIR = os.path.join('data', 'papers')
PAPER_FNAME = 'paper {0}.pdf' # paper <paper number>.pdf

ACM_DIR = os.path.join('data', 'acm-papers')
ACM_PAPER_FNAME = 'p{0}-{1}.pdf' # p<page number in main proceedings>-<author>.pdf

PROCEEDINGS_ONLY_NUMBERS_DIR = os.path.join('data', 'numbers')
PROCEEDINGS_ONLY_NUMBERS_PDF = os.path.join(PROCEEDINGS_ONLY_NUMBERS_DIR, 'numbers.pdf')
PROCEEDINGS_ONLY_NUMBERS_TEX = os.path.join(PROCEEDINGS_ONLY_NUMBERS_DIR, 'numbers.tex')

PROCEEDINGS_NAME = 'Proceedings_LAK_2019.pdf'
PROCEEDINGS_FRONT = 'front.pdf'