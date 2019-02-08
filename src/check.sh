#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: bash check.sh <path to pdf>"
    echo "Example: bash check.sh 'data/papers/paper_97.pdf'"
    exit 1
fi

# PDFTOTEXT
text=$(pdftotext "$1" -)
text_page_one=$(pdftotext -f 1 -l 1 "$1" -)
# FONTS
fonts=$(pdffonts "$1" 2>/dev/null)
# echo "$fonts"

abstract=$(echo "$text" | grep -c "ABSTRACT")
ccs=$(echo "$text" | grep -ic "CCS")
keywords=$(echo "$text" | grep -ic "KEYWORDS")
acmformat=$(echo "$text" | grep -ic "ACM Reference Format")
references=$(echo "$text" | grep -c "REFERENCES")
doi=$(echo "$text_page_one" | sed ':a;N;$!ba;s/\n/ /g' | egrep -oc "https: *//doi.org/10.1145/ *3303772\. *330")
venue=$(echo "$text_page_one" | sed ':a;N;$!ba;s/\n/ /g' | egrep -oc "March.*2019, Tempe,.*AZ, USA")

copyright1=$(echo "$text" | grep -i "2019 Copyright is held by")
copyright2=$(echo "$text" | grep -i "2019 Copyright held by")
copyright3=$(echo "$text" | grep -i "2019 Association for Computing Machinery")
copyright4=$(echo "$text" | grep -i "This article was authored by employees")

citationorder=$(echo "$text" | grep -o "\[[0-9]*]")

bad_fonts=$(echo "$fonts" | awk '{ print substr($0, 73, 3) }' | grep -c "no")
libertine_fonts=$(echo "$fonts" | grep -oc Libertine)
biolinum_fonts=$(echo "$fonts" | grep -oc Biolinum)
type3_fonts=$(echo "$fonts" | awk '{ print substr($0, 38, 18) }' | grep -c "Type 3")

echo "Paper: $1"
echo "Abstract: $abstract, References: $references"
echo "CCS Concepts: $ccs, Keywords: $keywords, ACM Format: $acmformat"
echo "DOI: $doi, Venue: $venue"
echo "Bad fonts: $bad_fonts, Libertine fonts: $libertine_fonts, Biolinum fonts: $biolinum_fonts, Type 3 fonts: $type3_fonts"

BADFonts=0
BadFormat=0

if [ "$bad_fonts" -ne 0 ]; then
    echo "Paper has embedded fonts!"
    BADFonts=$((BADFonts+1))
fi

if [ "$type3_fonts" -ne 0 ]; then
    echo "Paper contains type 3 fonts!"
    BADFonts=$((BADFonts+1))
fi

if [ "$libertine_fonts" -eq 0 -o "$biolinum_fonts" -eq 0 ]; then
    echo "Paper does not have Linux fonts!"
    BADFonts=$((BADFonts+1))
fi

if [[ -z $abstract ]]; then
    echo "Paper does not have ABSTRACT!"
    BadFormat=$((BadFormat+1))
fi

if [[ -z $ccs ]]; then
    echo "Paper does not have CCS CONCEPTS!"
    BadFormat=$((BadFormat+1))
fi

if [[ -z $keywords ]]; then
    echo "Paper does not have KEYWORDS!"
    BadFormat=$((BadFormat+1))
fi

if [[ -z $acmformat ]]; then
    echo "Paper does not have ACM Reference Format!"
    BadFormat=$((BadFormat+1))
fi

if [[ -z $references ]]; then
    echo "Paper does not have REFERENCES!"
    BadFormat=$((BadFormat+1))
fi

if [[ -z $copyright1 && -z $copyright2 && -z $copyright3 && -z $copyright4 ]]; then
    echo "Paper does not have 2019 Copyright!"
    BadFormat=$((BadFormat+1))
fi

if [[ $venue -ne 2 ]]; then
    echo "Paper does not have VENUE twice!"
    BadFormat=$((BadFormat+1))
fi

if [[ $doi -ne 2 ]]; then
    echo "Paper does not have DOI twice!"
    BadFormat=$((BadFormat+1))
fi

if [[ "$BADFonts" -eq 0 && "$BadFormat" -eq 0 ]]; then
    echo "Paper is Ok!"
else
    echo "Paper is NOT Ok"
    exit 1
fi