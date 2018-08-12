#!/usr/bin/env python

__author__ = "Satyendra Pandey"
__email__  = "pandeys@iitk.ac.in"


from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from glob import glob
from collections import Counter
import re, math, time
import numpy as np


# Defining some important things for future use
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")
WORD = re.compile(r'\w+')


# To get column of a 2d matrix it have been used in row to column transform 
def column(matrix, i):
    return [row[i] for row in matrix]


# To get word to vec well you can also call it word counter
def w2vec(data):
	temp = Counter(data)
	return temp	


# to convery list to a document
def l2doc(arr):
	res = {}
	for key, val in arr:
		res.update({str(key): val})
	return res


# to get cosine similarity of two arrays
def get_cosine(doc1, doc2):
	vec1 = w2vec(doc1)
	vec2 = w2vec(doc2)
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])
	sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
	sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)
	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator


# for subtitle parsing
def subsParse(filename):
	with open(filename, 'r') as tempReader:
		data = tempReader.read()
	defaultHeader = filename.split("/")[-1].split(".")[0]
	result = {"header": defaultHeader, "para": data}
	return result


# for tutorial parsing into different sections
def docParse(filename):
	result = []
	with open(filename, 'r') as tempReader:
		data = tempReader.read()
	headers = data.split('<header>')
	defaultHeader = [filename.split("/")[-1].split(".")[0]]
	for header in headers:
		temp_header = defaultHeader + re.findall("(.*?)</header>", header)
		temp_para =  re.findall("<para>(.*?)</para>", header)
		temp_header = " ".join(temp_header)
		temp_para = " ".join(temp_para)
		result.append({"header": temp_header, "para": temp_para})
	return result


# to preprocess the data
def preProcess(mess):
	# Converting to lower
	mess = mess.lower()
	# removing numbers other than alpha-numeric
	mess = WORD.findall(mess)
	mess = " ".join(mess)
	# tokenizing words
	word_tokens = word_tokenize(mess)
	# Removing stop_words
	word_tokens = [temp for temp in word_tokens if temp not in stop_words]
	# giving pos_tags and removing some pos
	pos = pos_tag(word_tokens, tagset='universal')
	# stemming the words
	pos = [stemmer.stem(word) for (word, tag) in pos if tag in ['NOUN', 'X']]
	# removing common words from youtube tutorials to reduce noise in result
	pos = [tword for tword in pos if tword not in cwords]
	string = " ".join(pos)
	return string, pos


# finding most common words from tutorial to remove that
# Like in youtube you'll commonly hear this term like guys, share, like, enjoy...
# give filenames as input, just download tutorials on some other topics too to find the useful common words
def commonAll(ytFiles):
	wlist = []
	for ytFile in ytFiles:
		result = subsParse(ytFile)
		doc1, arr = preProcess(result['para'])
		wlist += arr
	temp = w2vec(wlist)
	return temp	


# Already assign common word to be loaded which is in common.txt
def commonSpec(fileName):
	with open(fileName, 'r') as tempReader:
		mess = tempReader.read()
	mess = mess.lower()
	mess = WORD.findall(mess)
	return set(mess)	


# to find most common youtube word we will use html, javascript tutorials and see what's coming out
cwords = commonSpec("common_wrd.txt")



if __name__ == "__main__":
	
	doc = "The quick brown fox jumps over the lazy dog"
	line, arr = preProcess(doc)
	print line
	print arr
