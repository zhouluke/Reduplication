
# INFORMANT-ONLY TRANSCRIPT MAKER: CANADIAN SET
# Luke Zhou. May 2016.
# Run this on transcript sets whose speaker codes are given in 
# ANGULAR brackets (< >) and where closing tags are present (</000>).

import sys
import os, fnmatch
import re

if (len(sys.argv)<2+1):
	usage = "Usage: python mk-inf-can.py <in-directory> <out-directory> \n"
	usage += "Example: python mk-inf-can.py 'C:/CAN SET' 'C:/CAN - INF ONLY' "
	sys.exit(usage)

inDir = sys.argv[1] 
outDir = sys.argv[2] 


toDoManually = []	# Keeps track of the filenames with '&' in them


# Helper function: Finds all files (subject to 'filter') in the directory 'path'
# From: http://stackoverflow.com/questions/13299731
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


for textFile in findFiles(inDir, '*.txt'):

	inFile = open(textFile, 'r')

	# Saves the contents of the input file 
	text=inFile.read()
	inFile.close()	# Important: Closes the file ASAP!
	
	text = text.strip()
	if (not text):
		continue

	#text = text.decode('utf-8')

	text = re.sub(r"\n|\r"," ",text)	# replaces all line returns with spaces

	# e.g., '<3> ... </3>' -> ''
	text = re.sub(r"<[123456789]\d*>.*?</\d+>",r"",text) 

	# e.g., '[3] ... (tape ends)' -> '(tape ends)'
	#text = re.sub(r"<[^0]\d*>.*?(\((T|t)ape)",r"\1",text) 


	# Correcting for improper character encoding
	text = re.sub(r"\xD5","'",text)
	text = re.sub(r"","",text)
	text = re.sub(r"\x00","",text)

	# Contractions
	#text = re.sub(r"(\w+) '(s|ll|d|t|re|ve|m|z)",r"\1'\2",text) 

	# Adds appropriate spacing between bracketed things
	#text = re.sub(r"(\)|\]|-|\})(\(|\[|\{)",r"\1 \2",text) 

	# Collapses multiple spacing into a single space character
	text = re.sub(r" +",r" ",text) 


	# Output file
	tmp = textFile[textFile.index('/')+1:]
	outFileNm = outDir + "/" + tmp
	#print outFileNm

	if '&' in tmp or 'All_' in tmp:
		toDoManually.append(tmp)

	# Creates intermediate directories if they don't exist
	# Snippet from http://stackoverflow.com/a/12517490
	if not os.path.exists(os.path.dirname(outFileNm)):
		try:
			os.makedirs(os.path.dirname(outFileNm))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	outFile = open(outFileNm, 'w')
	outFile.write(text)
	outFile.close()


print ("THE FOLLOWING FILES MAY HAVE MULTIPLE SPEAKERS. PLEASE DO THEM MANUALLY:")
for fn in toDoManually:
	print (fn)