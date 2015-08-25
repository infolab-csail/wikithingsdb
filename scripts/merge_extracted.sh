#!/bin/sh

# Merges all files created by defexpand/scripts/WikiExtractor.py into
# one merged.xml file

if [ -d "$1" ] && [ -d "$2" ]; then
    echo "Merging all files under $1 into $2merged.xml"
    find $1 -name wiki_* -print0 | xargs -0 -I file cat file > $2/merged-tmp.xml

    echo "Inserting <root> at top of file"
    echo "<root>" > $2/begin-tmp
    cat $2/begin-tmp $2/merged-tmp.xml > $2/merged.xml
    rm -f $2/begin-tmp 
    rm -f $2/merged-tmp.xml

    echo "Inserting </root> end of file"
    echo "</root>" >> $2/merged.xml
    echo "DONE."
else
    echo "Usage: ./merge_extracted.sh /path/to/extracted/ /path/to/output/dir"
fi
