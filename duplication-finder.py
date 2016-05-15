
import sys
import os, fnmatch
import re

if (len(sys.argv)<1+1):
	usage = "Usage: python ngram-maker.py <in-directory>\n"
	usage += "Example: python ngram-maker.py 'C:/INFORMANT ONLY TRANSCRIPTS'"
	sys.exit(usage)

inDir = sys.argv[1] 
#outDir = sys.argv[2] 
#n = int(sys.argv[3])


# Helper function: Finds all files (subject to 'filter') in the directory 'path'
# From: http://stackoverflow.com/questions/13299731
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)

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

	# Output file
	'''outFileNm = outDir + "/" + textFile[textFile.index('/')+1:]
	print outFileNm

	# Snippet from http://stackoverflow.com/a/12517490
	if not os.path.exists(os.path.dirname(outFileNm)):
		try:
			os.makedirs(os.path.dirname(outFileNm))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	outFile = open(outFileNm, 'w')'''
	
	
	for line in lines:

		words = line.split(" ")
		
		numWds = len(words)
		newLine = ""

		for i in range(0,numWds-1):

			word = words[i].lower()
			nxtWord = words[i+1].lower()

			if '(inc)' in word:
				continue

			if len(word)>1 and (word == nxtWord):

				#print(word + " " + nxtWord + "\t" + line)

				toAppend = speaker + "\t" + line

				if word not in found:
					found[word] = []
				found[word].append(toAppend)

	#outFile.close()

	#print "========================================="



#sorted_finds = [x for x in found.iteritems()] 
#sorted_finds.sort(key=lambda x: x[0]) # sort by key

keys = found.keys()

# Prints out a list of all reduplications
for key in sorted(keys):
	print key +" "+ key

print "===================================="

# Prints out a list of all reduplications WITH the contexts & speakers
for key in sorted(keys): 
    print key +" "+ key 
    for v in found[key]:
    	print "\t" + v
    print "===================================="

