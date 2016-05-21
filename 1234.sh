#!/bin/bash

for i in {1..4} 
do
	#: '
	echo "Pre-processing $i-grams"
	time python ngram-preproc.py transcr ${i}grammed $i > /dev/null
	echo ""
	#'

	echo "Searching for $i-gram reduplications"
	time python duplication-finder.py ${i}grammed $i >  ${i}gram-dupes.txt
	echo ""
done