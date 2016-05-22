
# INFORMANT-ONLY TRANSCRIPT MAKER: UK SET
# Luke Zhou. May 2016.
# Run this on transcript sets whose speaker codes are given in 
# SQUARE brackets ([ ]) and where NO closing tags are present.

import sys
import os, fnmatch
import re
import infHelpers as helpers

if (len(sys.argv)<2+1):
	usage = "Usage: python mk-inf-uk.py <in-directory> <out-directory> \n"
	usage += "Example: python mk-inf-uk.py 'C:/UK SET' 'C:/UK - INF ONLY' "
	sys.exit(usage)

inDir = sys.argv[1] 
outDir = sys.argv[2] 


multiSpkrs = []	# Keeps track of the filenames with '&' in them


def killSqTags(text):

	# e.g., '[3] ... [003]' -> '[003]'
	text = re.sub(r"\[[^0]\d*\].*?(\[0)",r"\1",text) 

	# e.g., '[3] ... (tape ends)' -> '(tape ends)'
	text = re.sub(r"\[[^0]\d*\].*?(\((T|t)ape)",r"\1",text) 

	return text


######################################
# MAIN METHOD
######################################

for textFile in helpers.findFiles(inDir, '*.txt'):

	result = helpers.doOneFile(textFile,outDir,killSqTags)

	if result!=0:
		multiSpkrs.append(result)


print ("THE FOLLOWING FILES MAY HAVE MULTIPLE SPEAKERS. PLEASE DO THEM MANUALLY:")
for fn in multiSpkrs:
	print (fn)