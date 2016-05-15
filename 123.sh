
#time python ngram-preproc.py transcr 1grammed 1 > /dev/null
#time python duplication-finder.py 1grammed >  1gram-dupes.txt

time python ngram-preproc.py 1grammed 2grammed 2 > /dev/null
time python duplication-finder.py 2grammed >  2gram-dupes.txt

time python ngram-preproc.py 1grammed 3grammed 3 > /dev/null
time python duplication-finder.py 3grammed >  3gram-dupes.txt
