#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: bash ghostscript.sh <path to pdf> <path to fonts separated with ;> <path to output>"
    echo "Example: bash ghostscript.sh 'data/papers/paper_97.pdf' /Library/Fonts/ArialMT.ttf;/Library/Fonts/Helvetica.ttf' 'data/papers/97_fixed.pdf'"
    exit 1
fi

ghostscript                       \
  -o "$3"                         \
  -sDEVICE=pdfwrite               \
  -dEmbedAllFonts=true            \
  -sFONTPATH="$2"                 \
  "$1"
