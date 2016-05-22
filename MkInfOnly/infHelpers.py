
# INFORMANT-ONLY TRANSCRIPT MAKERS: HELPER FUNCTIONS
# Luke Zhou. May 2016.

import os, fnmatch
import re

# Helper function: Finds all files (subject to 'filter') in the directory 'path'
# From: http://stackoverflow.com/questions/13299731
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)

# Writes the contents of 'text' to the file whose name is 'outFileNm'
def writeOut(outFileNm,text):

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


# Reads in a single file like '<inDir>/YORK/lol.txt', removes tags and other
# nasty things, and then writes the modified version to '<outDir>/YORK/lol.txt'
# Returns: 	0 if there is only one speaker in this file; 
#			1 if the contents of this file are empty;
# 			the name of the speaker file if there are multiple speakers.
def doOneFile(textFile,outDir,tagKillingFn):

	inFile = open(textFile, 'r')

	# Saves the contents of the input file 
	text=inFile.read()
	inFile.close()	# Important: Closes the file ASAP!
	
	text = text.strip()
	if (not text):
		#continue
		return 0

	#text = text.decode('utf-8')

	text = re.sub(r"\n|\r"," ",text)	# replaces all line returns with spaces
	
	# Correcting for improper character encoding
	text = re.sub(r"\xD5","'",text)
	text = re.sub(r"","",text)
	text = re.sub(r"\x00","",text)

	text = tagKillingFn(text)

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

	writeOut(outFileNm,text)

	if '&' in tmp or 'All_' in tmp:
		#toDoManually.append(tmp)
		return tmp

	return 0