
# INFORMANT-ONLY TRANSCRIPT MAKER: ANGULAR TAG SET
# Luke Zhou. May 2016.
# Run this on transcript sets whose speaker codes are given in 
# ANGULAR brackets (< >) and where closing tags are present (</000>).

import sys
import os, fnmatch
import re
import infHelpers as helpers

if (len(sys.argv)<2+1):
	usage = "Usage: python mk-inf-ang.py <in-directory> <out-directory> \n"
	usage += "Example: python mk-inf-ang.py 'C:/CAN SET' 'C:/CAN - INF ONLY' "
	sys.exit(usage)

inDir = sys.argv[1] 
outDir = sys.argv[2] 


multiSpkrs = []	# Keeps track of the filenames with '&' in them


def killAngTags(text):

	# e.g., '<3> ... </3>' -> ''
	text = re.sub(r"<[123456789]\d*>.*?</\d+>",r"",text) 

	# e.g., '[3] ... (tape ends)' -> '(tape ends)'
	#text = re.sub(r"<[^0]\d*>.*?(\((T|t)ape)",r"\1",text)

	return text


######################################
# MAIN METHOD
######################################

for textFile in helpers.findFiles(inDir, '*.txt'):

	result = helpers.doOneFile(textFile,outDir,killAngTags)

	if result!=0:
		multiSpkrs.append(result)


print ("THE FOLLOWING FILES MAY HAVE MULTIPLE SPEAKERS. PLEASE DO THEM MANUALLY:")
for fn in multiSpkrs:
	print (fn)