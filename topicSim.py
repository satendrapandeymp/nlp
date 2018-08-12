import gensim
from gensim import corpora
from langProcessing import docParse, preProcess, cwords, subsParse, get_cosine, column, l2doc
from glob import glob


Lda = gensim.models.ldamodel.LdaModel


if __name__ == "__main__":
	
	# To get the filenames from the directory
	tuteFiles = sorted(glob("Tutorials/*"))
	ytFolders = sorted(glob("Results/*"))

	# Process tutorials point document 
	procTutes = []
	allWord = []
	for tuteFile in tuteFiles:
		singleTute = []
		result = docParse(tuteFile)
		for count, res in enumerate(result):
			doc_para, arr_para = preProcess(res['para'])
			doc_header, arr_header = preProcess(res['header'])
			singleTute.append({'para': arr_para, 'header': arr_header})
			allWord.append(arr_para + arr_header)			
		procTutes.append(singleTute)
	
	# to get model of topics using texts from tutorial points
	dictionary = corpora.Dictionary(allWord) 	
	doc_term_matrix = [dictionary.doc2bow(doc) for doc in allWord]
	ldamodel = Lda(doc_term_matrix, num_topics=len(tuteFiles), id2word = dictionary, passes=500)

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
					subHeader = dictionary.doc2bow(procSub['header'])
					subPara   = dictionary.doc2bow(procSub['para'])
					tutHeader = dictionary.doc2bow(section['header'])
					tutPara   = dictionary.doc2bow(section['para'])

					temp_res += 2 * get_cosine(l2doc(ldamodel[subHeader]) , l2doc(ldamodel[tutHeader]))
					temp_res += 5 * get_cosine(l2doc(ldamodel[tutPara]) ,   l2doc(ldamodel[subPara]))
					temp_res +=     get_cosine(l2doc(ldamodel[subHeader]) , l2doc(ldamodel[tutPara]))
					temp_res +=     get_cosine(l2doc(ldamodel[subPara]) ,   l2doc(ldamodel[tutHeader]))
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
	with open("Out/resTopic.csv", 'w') as writer:	
		for matchRes in mfinalRes:
			tempStr = matchRes[0]["tutorialFile"] + "\t"
			for files in matchRes:
				tempStr += "".join(files["matchedFile"].split("/")[-1].split(".")[0].split()) + "\t" + str(files["Score"]) + "\t"
			
			tempStr += "\n"
			writer.write(tempStr)
			
