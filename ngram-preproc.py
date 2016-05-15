
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
	outFileNm = outDir + "/" + textFile[textFile.index('/')+1:]
	print outFileNm

	# Snippet from http://stackoverflow.com/a/12517490
	if not os.path.exists(os.path.dirname(outFileNm)):
		try:
			os.makedirs(os.path.dirname(outFileNm))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	outFile = open(outFileNm, 'w')
	
	# For each line, makes n-grams out of the words!
	for line in lines:
		
		line = re.sub("\[(\d|:|\.)+\]","",line)	# timecodes
		line = re.sub(r"-|\'|\"|\,|","",line) # punctuation
		line = re.sub(r"(</?\d+>\s*</?\d+>)|\.|\?|!","\n",line) # tags & sentence breaks
		line = re.sub(r"(<\d+><\d+>)","",line)

		# Corrects for improper character encoding
		line = re.sub(r"\xD5","'",line)
		line = re.sub(r"","",line)
		line = re.sub(r"\x0ngram0","",line)

		words = line.split(" ")
		
		numWds = len(words)
		newLine = ""

		try:
			for i in range(0,numWds-n-1):

				for j in range(0,n):
					word = words[i+j]
					if word == '\n':
						j = j+1
					newLine = newLine + word
				newLine = newLine + " "

		#print newLine
		outFile.write(newLine)

	outFile.close()