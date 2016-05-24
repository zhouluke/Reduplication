
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

def mkOutFileNm(inFileNm):
	
	outFileNm = inFileNm[inFileNm.index('/')+1:]
	#outFileNm = outDir + "/" + nmWithoutDir
	return outFileNm

###############################################

# Precondition: assumes interviewer tags have already been removed
def filterBySpeakers(text,tagKillingFn,openTag,closeTag):

	# Regex-safe versions of the open/close tags
	openTagRgx = '\\' + openTag
	closeTagRgx = '\\' + closeTag

	rgxForIDs = openTagRgx + r'(\d+)' + closeTagRgx	# e.g., \[045\] -> 045
	#print rgxForIDs

	remTags = re.findall(rgxForIDs,text)
	if not remTags:	# cannot speaker tags
		return None

	remTags = set(remTags)
	#print remTags

	# Placeholders to assist with the find & replace process
	SPKR_TMP = 'PLACEHOLDER'
	NONSPKR_TMP = openTag + '8' + closeTag	# something that would get pruned by tagKillingFn
	NONSPKR_TMP_RGX = openTagRgx + '8' + closeTagRgx


	# Dictionary to map speaker IDs to filtered transcripts 
	filtered = {}	 

	for spkID in remTags:
		
		myTag = openTag+spkID+closeTag
		myTagRgx = openTagRgx+spkID+closeTagRgx

		textCpy = re.sub(myTagRgx,SPKR_TMP,text)	# protects ID of target spaker
		textCpy = re.sub(rgxForIDs,NONSPKR_TMP,textCpy)	# renames non-targets
		textCpy = re.sub(SPKR_TMP,myTag,textCpy)	# restores target speaker

		textCpy = tagKillingFn(textCpy)

		textCpy = re.sub(r" +",r" ",textCpy)	# collapses extra spaces into one

		# Check that the filtering really killed all other speakers
		lingerers = re.findall(NONSPKR_TMP_RGX,text)
		if lingerers:
			print "WARNING! Other speakers found in filtered transcript for speaker " + spkID
			for x in lingerers:
				print "\t" + x

		filtered[spkID] = textCpy
		#print textCpy

	return filtered


###############################################

def normalizeTxt(text):
	return text

# Reads in a single file like '<inDir>/YORK/lol.txt',
# then removes tags and normalizes the texts.
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

	'''
	# Contractions
	#text = re.sub(r"(\w+) '(s|ll|d|t|re|ve|m|z)",r"\1'\2",text) 

	# Adds appropriate spacing between bracketed things
	#text = re.sub(r"(\)|\]|-|\})(\(|\[|\{)",r"\1 \2",text) 
	'''

	# Collapses multiple spacing into a single space character
	text = re.sub(r" +",r" ",text) 

	return text
