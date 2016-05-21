
import sys
import os, fnmatch
import re

if (len(sys.argv)<2+1):
	usage = "Usage: python ngram-maker.py <in-directory> <n> \n"
	usage += "Example: python ngram-maker.py 'C:/INFORMANT ONLY TRANSCRIPTS'"
	sys.exit(usage)

inDir = sys.argv[1] 
#outDir = sys.argv[2] 
n = int(sys.argv[2])

JOINER = '*'
PUNCT = ['-','"',':','(',')',';'] # not included: ','


# Helper function: Finds all files (subject to 'filter') in the directory 'path'
# From: http://stackoverflow.com/questions/13299731
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


# Kills likely false positives
def isFalsePositive(ngram):

	'''if '(inc)' in ngram:
		return True

	words = ngram.split(JOINER)

	i=0
	for word in words:

		if len(word)<=1:
			return True
		if word[-1] in PUNCT or word[0] in PUNCT:
			return True
		# Handles comma differently depending on whether n=1 or n>1 -_-
		if word[-1]==',':
			if n==1:
				return True	
			# Gets mad when ',' is in the middle of a MULTIgram, 
			# but not when it's at the end
			if i<len(words)-1:
				return True	

		i = i+1'''

	return False

#######################################################################

found = {}	# maps reduplicates to speakers & utterances
counts = {}	# maps reduplicates to frequency counts

for textFile in findFiles(inDir, '*.txt'):
	
	#print(textFile)

	speaker = textFile[textFile.rfind('/')+1:]
	speaker = re.sub("_\d+\.txt\s*$","",speaker)	# numbers @ end of filenames
	speaker = re.sub("\.txt\s*$","",speaker)	
	speaker = re.sub(r"^\d+(_|-)(\d-)?","",speaker)	# numbers at start of filenames
	#print speaker

	inFile = open(textFile, 'r')
	# Saves the contents of the input file into an array
	lines=[]
	for line in inFile:

		line = line.strip()
		if (not line):
			continue

		#line = line.decode('utf-8')
		lines.append(line)

	inFile.close()	# Important: Closes the file ASAP!


	# OUTPUT:
	for line in lines:

		origLine = line

		ngrams = line.split(" ")
		
		numNgrams = len(ngrams)

		for i in range(0,numNgrams-n):

			ngram = ngrams[i].lower()
			nxtNgram = ngrams[i+n].lower()

			if isFalsePositive(ngram):
				continue

			if (ngram.replace(',','') == nxtNgram.replace(',','')):

				toAppend = speaker + "\t" + origLine

				key = ngram.replace(JOINER,' ')

				if key not in found:
					found[key] = []
					counts[key] = 0

				found[key].append(toAppend)
				counts[key] = counts[key] + 1


# FINAL REPORTING

# Sort by frequency
'''counts_sorted = [x for x in counts.iteritems()] 
counts_sorted.sort(key=lambda x: x[1]) # sort by value
counts_sorted.reverse()

# Prints out a list of all reduplications & counts
for x in counts_sorted:
	print x[0] +" "+ x[0] + "\t" + str(x[1])

print "===================================="

# Prints out a list of all reduplications WITH the contexts & speakers
for x in counts_sorted: 

	key = x[0]
	freq = str(x[1])
	print key +" "+ key + "\t" + freq

	for v in found[key]:
		tmp = v.split(" ")
		lastWord = tmp[-1]
		# Output words in the sentence, not n-grams!
		tmp = map(lambda(x):(x[0:x.index(JOINER)]) if JOINER in x else x, tmp)
		tmp = tmp + lastWord.split(JOINER)[1:]
		print "\t" + " ".join(tmp) 
	print "===================================="
'''

# Sort by alphabetical order
keys = found.keys()
  
# Prints out a list of all reduplications & counts
for key in sorted(keys):
	print key +" "+ key + "\t" + str(counts[key])

print "===================================="

# Prints out a list of all reduplications WITH the contexts & speakers
for key in sorted(keys): 

	print key +" "+ key 

	for v in found[key]:
		tmp = v.split(" ")
		lastWord = tmp[-1]
		# Output words in the sentence, not n-grams!
		tmp = map(lambda(x):(x[0:x.index(JOINER)]) if JOINER in x else x, tmp)
		tmp = tmp + lastWord.split(JOINER)[1:]
		print "\t" + " ".join(tmp) 
	print "===================================="