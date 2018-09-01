#!/usr/bin/env python

__author__ = "Satyendra Pandey"
__email__  = "pandeys@iitk.ac.in"
__doc__ = "I'm going to use keywords in the center of this algo, Just by using this I'm hoping a hugh performence boost"


from langProcessing import docParse, preProcess, cwords, subsParse, get_cosine, column
from gettingSub import gettingSub
from glob import glob

def gettingVid(para, header):
    score = []
    obj = gettingSub( " ".join(list(set(header))), "Video")
    obj.Get_subtitle()
    flist = sorted(glob("Results/" + " ".join(list(set(header))) + "/*"))
    for fname in flist:
        result = subsParse(fname)
        doc_para, arr_para = preProcess(result['para'])
        doc_header, arr_header = preProcess(result['header'])
        temp_res = 2 * get_cosine(header , arr_header)
        temp_res += 5 * get_cosine(para , arr_para)
        temp_res += get_cosine(header , arr_para)
        temp_res += get_cosine(para , arr_header)
        score.append({"score": temp_res, "vid": result["vid"], "title": result['header']})
    score.sort(key=lambda x:x["score"], reverse=True )
    return score[:5]

def thirdAlgo():
	
	# To get the filenames from the directory
	tuteFiles = sorted(glob("Tutorials/*"))

	# To save the results
	outStream = open("Out/thAlgo.csv", "w")
	outStream.write("Title\tScore\tytubeLink\tvideoTitle\n")

	# Process tutorials point document
	for tuteFile in tuteFiles:
		result = docParse(tuteFile)
		para, header = [], []
		for res in result:
			doc_para, arr_para = preProcess(res['para'])
			doc_header, arr_header = preProcess(res['header'])
			para += arr_para
			header += arr_header
        
		# to get videos with similar topics
		temp_res = gettingVid(para,header)
		for res in temp_res:
			out = "{0}\t{1}\thttps://www.youtube.com/watch?v={2}\t{3}\n".format(tuteFile.split("/")[1].split(".")[0], res["score"], res["vid"], res["title"])
			outStream.write(out)

	outStream.close()
