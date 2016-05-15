
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
PUNCT = ['-',',','"',':','(',')']


# Helper function: Finds all files (subject to 'filter') in the directory 'path'
# From: http://stackoverflow.com/questions/13299731
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


# Kills likely false positives
def isFalsePositive(ngram):

	if '(inc)' in ngram:
		return True

	words = ngram.split(JOINER)

	for word in words:
		if len(word)<=1 or word[-1] in PUNCT or word[0] in PUNCT:
			return True

	return False

#######################################################################

found = {}


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

		words = line.split(" ")
		
		numWds = len(words)
		newLine = ""

		for i in range(0,numWds-n):

			word = words[i].lower()
			nxtWord = words[i+n].lower()

			if isFalsePositive(word):
				continue

			if (word == nxtWord):

				#print(word + " " + nxtWord + "\t" + line)

				toAppend = speaker + "\t" + line

				key = word.replace(JOINER,' ')
				if key not in found:
					found[key] = []
				found[key].append(toAppend)


# FINAL REPORTING

#sorted_finds = [x for x in found.iteritems()] 
#sorted_finds.sort(key=lambda x: x[0]) # sort by key

keys = found.keys()

# Prints out a list of all reduplications & counts
for key in sorted(keys):
	print key +" | "+ key + "\t" + str(len(found[key]))

print "===================================="

# Prints out a list of all reduplications WITH the contexts & speakers
for key in sorted(keys): 
    print key +" | "+ key 
    for v in found[key]:
    	tmp = v.split(" ")
    	lastWord = tmp[-1]
    	# Output words in the sentence, not n-grams!
    	tmp = map(lambda(x):(x[0:x.index(JOINER)]) if JOINER in x else x, tmp)
    	tmp = tmp + lastWord.split(JOINER)[1:]
    	print "\t" + " ".join(tmp) 
    print "===================================="

