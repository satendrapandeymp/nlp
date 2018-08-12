#!/usr/bin/env python

__author__ = "Satyendra Pandey"
__email__  = "pandeys@iitk.ac.in"


from langProcessing import docParse, preProcess, cwords, subsParse, get_cosine, column
from glob import glob


if __name__ == "__main__":
	

	# To get the filenames from the directory
	tuteFiles = sorted(glob("Tutorials/*"))
	ytFolders = sorted(glob("Results/*"))

	# Process tutorials point document
	procTutes = []
	for tuteFile in tuteFiles:
		singleTute = []
		result = docParse(tuteFile)
		for res in result:
			doc_para, arr_para = preProcess(res['para'])
			doc_header, arr_header = preProcess(res['header'])
			singleTute.append({'para': arr_para, 'header': arr_header})
		procTutes.append(singleTute)


	# FINAL RESULT
	finalRes = [] 

	# now we will check it against all of the tutorials
	# Here I am assuming that most of thr tutorials must have some good resources on each topic
	for ytFolder in ytFolders:

		# Iterate through all the folders
		ytFiles = sorted(glob(ytFolder + "/*")) 	


		# To process the data of a selected youtube tutorial folder
		procSubs = []
		for ytFile in ytFiles:
			result = subsParse(ytFile)
			doc_para, arr_para = preProcess(result['para'])
			doc_header, arr_header = preProcess(result['header'])
			procSubs.append({'para': arr_para, 'header': arr_header})


		# find cosine similarity for all of the tutorialpoint documents
		tempRes = []
		for countTute, procTute in  enumerate(procTutes):			
			result = []
			for countSub, procSub in enumerate(procSubs):
				temp_res = 0
				for section in procTute:
					temp_res += 2 * get_cosine(procSub['header'] , section['header'])
					temp_res += 5 * get_cosine(procSub['para'] , section['para'])
					temp_res += get_cosine(procSub['header'] , section['para'])
					temp_res += get_cosine(procSub['para'] , section['header'])
				result.append({"score": temp_res, "file": ytFiles[countSub]})
			result.sort(key=lambda r:r["score"])
			tempRes.append({ "tutorialFile": tuteFiles[countTute].split("/")[-1], "matchedFile":  result[-1:][0]["file"], "Score": result[-1:][0]["score"]})

		finalRes.append(tempRes)		
			
	mfinalRes = []	
	for i in range(len(tuteFiles)):
		temp = column(finalRes, i)
		temp.sort(key=lambda r:r["Score"])
		mfinalRes.append(temp[-5:])

	print mfinalRes[0]

	# Finally writing the result in a csv format
	with open("Out/resDoc.csv", 'w') as writer:	
		for matchRes in mfinalRes:
			tempStr = matchRes[0]["tutorialFile"] + "\t"
			for files in matchRes:
				tempStr += "".join(files["matchedFile"].split("/")[-1].split(".")[0].split()) + "\t" + str(files["Score"]) + "\t"
			
			tempStr += "\n"
			writer.write(tempStr)
			
