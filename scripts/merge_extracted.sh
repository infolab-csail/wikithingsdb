#!/bin/sh

# Merges all files created by defexpand/scripts/WikiExtractor.py into
# one merged.xml file

if [ -d "$1" ] && [ -d "$2" ]; then
    date
    echo "Merging all files under $1 into $2merged.xml"
    find $1 -name wiki_* -print0 | xargs -0 -I file cat file > $2/merged.xml

    echo "Replacing & with &amp;"
    sed -i 's/&/&amp;/g' $2/merged.xml

    echo "Deleting all <br> tags"
    sed -i 's/<br>//g' $2/merged.xml

    echo "Deleting all </br> tags"
    sed -i 's#</br>##g' $2/merged.xml

    echo "DONE."
    date
else
    echo "Usage: ./merge_extracted.sh /path/to/extracted/ /path/to/output/dir"
fi
