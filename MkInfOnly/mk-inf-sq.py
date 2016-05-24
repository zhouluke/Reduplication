
# INFORMANT-ONLY TRANSCRIPT MAKER: SQUARE TAG SET
# Luke Zhou. May 2016.
# Run this on transcript sets whose speaker codes are given in 
# SQUARE brackets ([ ]) and where NO closing tags are present.

import sys
import os, fnmatch
import re
import infHelpers as helpers

if (len(sys.argv)<2+1):
	usage = "Usage: python mk-inf-sq.py <in-directory> <out-directory> \n"
	usage += "Example: python mk-inf-sq.py 'C:/UK SET' 'C:/UK - INF ONLY' "
	sys.exit(usage)

inDir = sys.argv[1] 
outDir = sys.argv[2] 


multiSpkrs = []	# Keeps track of the filenames with '&' in them


######################################
# HELPER FUNCTIONS
######################################

def killSqTags(text):

	# e.g., '[3] ... [003]' -> '[003]'
	text = re.sub(r"\[[^0]\d*\].*?(\[0)",r"\1",text) 

	# e.g., '[3] ... (tape ends)' -> '(tape ends)'
	text = re.sub(r"\[[^0]\d*\].*?((\(|{)(T|t)ape)",r"\1",text) 

	# e.g., '[3] ... (Interview ends)' -> '(Interview ends)'
	text = re.sub(r"\[[^0]\d*\].*?((\(|{)(I|i)nterview)",r"\1",text) 

	# e.g., '[3] ... [4]' -> ''
	text = re.sub(r"\[[^0]\d*\].*?\[[^0]\d*\]","",text) 

	return text


######################################
# MAIN METHOD
######################################

print ("\nFILES GENERATED:\n")

tagKillFn = killAngTags

for textFile in helpers.findFiles(inDir, '*.txt'):

	text = helpers.doOneFile(textFile,outDir,tagKillFn)

	# Output file
	outFileNm = helpers.mkOutFileNm(textFile)
	outFilePath = outDir + "/" + outFileNm
	print outFileNm

	helpers.writeOut(outFilePath,text)

	# If there are multiple speakers in the file
	if '&' in outFileNm or 'All_' in outFileNm:
		
		multiSpkrs.append(outFileNm)
		
		fnBase = outFilePath[:-4]
		#print fnBase

		filtered = helpers.filterBySpeakers(text,tagKillFn,'[',']')

		# Writes filtered transcripts into new files (one per speaker)
		if filtered:
			for spkID, transcr in filtered.iteritems():
				newFileNm = fnBase+"_"+str(spkID)+".txt"
				helpers.writeOut(newFileNm, transcr)
				print "\t" + helpers.mkOutFileNm(newFileNm)


'''
print ("THE FOLLOWING FILES MAY HAVE MULTIPLE SPEAKERS. PLEASE DO THEM MANUALLY:")
for fn in multiSpkrs:
	print (fn)
'''