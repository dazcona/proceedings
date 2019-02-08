#!/usr/bin/python

import csv
import os
import re
import config

def read_papers():

    filename = os.path.join('data', config.PAPERS_CSV)

    output = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Emails
            emails = [ row['Lead Author e-mail'] ]
            emails.extend( row['Author e-mail;Author e-mail'].split(";") )
            # Row
            output.append(
                dict(
                    number = row['paper number'],
                    type = row['Paper Type'],
                    title = row['Title'],
                    author_names = row['Lead Author:Affiliation;Author2:Affiliation;Author3:Affiliation;etc.'].split(";"),
                    author_emails = emails,
                )
            )

    return output


def get_paper_numbers():

    papers = read_papers()

    return [ paper['number'] for paper in papers ]


def get_paper_titles():

    papers = read_papers()

    return [ paper['title'] for paper in papers ]


def read_papers_in_proceedings_order():

    papers = read_papers()

    filename = os.path.join('data', config.SCHEDULE_TXT)

    papers_in_order = []

    with open(filename) as f:

        lines = f.readlines()

        for line in lines:

            # Line
            line = line.strip()
            if line == '' or line.startswith('#') or '. Session' in line or '[Practicioner]' in line or '[AIED Best Paper]' in line: # do not add
                continue
            
            # Title
            title = line.split(';')[0].strip()

            matching_papers = [ paper for paper in papers if paper['title'].lower() == title.lower() ]
            
            paper = matching_papers[0] # will raise an exception if none found
            papers_in_order.append(paper)

    print('Number of papers in order: {0}'.format(len(papers_in_order)))

    return papers_in_order


def read_acm():

    filename = os.path.join('data', config.ACM_CSV)

    output = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Row
            strip = row['Title']
            output.append(
                dict(
                    number = row['ACM No.'],
                    type = row['Contact No.'],
                    strip = strip,
                    copyright = extract_match(strip, 'setcopyright{(.*?)}'),
                    book = extract_match(strip, 'acmBooktitle{(.*?)}'),
                    conference = extract_match(strip, 'acmConference(.*)acmBooktitle')[:-1],
                    short_doi = extract_match(strip, 'acmDOI{(.*?)}'),
                    price = extract_match(strip, 'acmPrice{(.*?)}'),
                    author = row['Author'],
                    email = row['Email'],
                    rights = row['Rights Granted'],
                    third_party = row['Third Party'],
                    material = row['Aux. Material'],
                    artistic_img = row['Artistic Images'],
                    govt_employees = row['Govt. Employees'],
                    open_access = row['Open Access'],
                    doi = row['DOI'],
                    authorizer = row['Authorizer'],
                    statement = row['Statement'],
                    cc_license = row['CC License'],
                    non_acm_copyright = row['Non-ACM Copyright'],
                )
            )

    return output


def extract_match(s, regex):

    p = re.compile(regex)
    matches = p.findall(s)
    if len(matches): 
        return matches[0]