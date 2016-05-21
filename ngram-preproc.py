
import sys
import os, fnmatch
import re

if (len(sys.argv)<3+1):
	usage = "Usage: python ngram-maker.py <in-directory> <out-directory> <n>\n"
	usage += "Example: python ngram-maker.py 'C:/INFORMANT ONLY TRANSCRIPTS' 'C:/2-GRAMMED' 2"
	sys.exit(usage)

inDir = sys.argv[1] 
outDir = sys.argv[2] 
n = int(sys.argv[3])


# Helper function: Finds all files (subject to 'filter') in the directory 'path'
# From: http://stackoverflow.com/questions/13299731
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


for textFile in findFiles(inDir, '*.txt'):
	
	# print(textFile)

	inFile = open(textFile, 'r')

	# Saves the contents of the input file 
	text=inFile.read()
	inFile.close()	# Important: Closes the file ASAP!
	
	text = text.strip()
	if (not text):
		continue

	#text = text.decode('utf-8')

	text = re.sub("\[(\d|:|\.)+\]","",text)	# timecodes
	#text = re.sub(r"\'|\"|\,|","",text) # punctuation

	text = re.sub(r"(</?\d+>\s*</?\d+>)","\n",text) # tag sandwiches -> sentence breaks
	text = re.sub(r"\.|\?|!","\n",text) # more sentence breaks
	text = re.sub(r"</?\d+>","",text)	# unsandwiched tags

	# Correcting for improper character encoding
	text = re.sub(r"\xD5","'",text)
	text = re.sub(r"","",text)
	text = re.sub(r"\x00","",text)

	# Contractions
	text = re.sub(r"(\w+) '(s|ll|d|t|re|ve|m|z)",r"\1'\2",text) 



	# Output file
	outFileNm = outDir + "/" + textFile[textFile.index('/')+1:]
	print outFileNm

	writeBuffer = ""
	

	# For each line, makes n-grams out of the words!
	lines = text.split("\n")
	lines = map(lambda(x):x.strip(),lines)

	for line in lines:

		if not line:
			continue
		#print "Line: " + line

		words = line.split(" ")
		numWds = len(words)
		newLine = ""

		# For each word x_i in the line, make the string x_i x_(i+1) ... x(i+n-1)
		for i in range(0,numWds-n+1):
			ngram = words[i:i+n]
			#print ngram

			'''if '\n' in ngram:
				newLine = newLine + '\n'
				print 'omg'
				continue'''

			newLine = newLine + ('*'.join(ngram)) + " "
		
		#print "New line: " + newLine[:-1]
		writeBuffer = writeBuffer + newLine[:-1] + "\n"


	# Flushes the write buffer to disk

	# Creates intermediate directories if they don't exist
	# Snippet from http://stackoverflow.com/a/12517490
	if not os.path.exists(os.path.dirname(outFileNm)):
		try:
			os.makedirs(os.path.dirname(outFileNm))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	outFile = open(outFileNm, 'w')
	outFile.write(writeBuffer)
	outFile.close()