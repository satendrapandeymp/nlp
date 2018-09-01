#!/usr/bin/env python

__author__ = "Satyendra Pandey"
__email__  = "pandeys@iitk.ac.in"


import urllib, os, time, sys
from bs4 import BeautifulSoup as Soup
from googlesearch import search

# setting default encoding as utf-8 so encodeing problem doesn't come
reload(sys)
sys.setdefaultencoding("utf-8")


# Defining class to scrap data from google through various links
class textMining:
	
	# To intialise the class
	def __init__(self, seed = None):
		if seed == None:
			raise Exception("Please give the keyword to proceed with google")
		self.seed = seed
		self.result = []
		self.__CheckDir("googleRes")

	
	# To get Insight in the elemnts
	def __inspect(self, html_content):
		with open('temp.html', 'w') as temp_writer:
			temp_writer.write(html_content)
		print "Please open the temp.html file to see if there is any error..."

	
	# To make directory in case if that is not present
	def __CheckDir(self, Name):
		if not os.path.exists(Name):
			os.mkdir(Name)


	# To write the result in specified file
	def __writer(self, string, name, seed):
		with open(name, 'w') as temp_writer:
			temp_writer.write(string)
		with open("linkSub.csv", 'a') as temp:
			temp.write("".join(name.split("/")[-1].split(".")[0].split()) + "\t" + seed + "\n")


	# To save the subtitle result into text file in Tutorials directory
	def __downloadData(self, seed, name):
		try:
			temp = urllib.urlopen(seed)
			Page_Html = temp.read()
			Parsed_html = Soup(Page_Html, 'html.parser')
			paras = Parsed_html.findAll("p")
			headers = Parsed_html.findAll("h2")		
			temp_str = ""
			for tempStr in paras:
				temp_str += tempStr.text
			self.__writer(temp_str, name, seed)
		except:
			pass


	# To get the basic link to all the other portions of that given tutorial 	
	def getList(self):
		for link in search(self.seed, tld="com", num=10, stop=1, pause=2):
			print link
			self.result.append({"link": link, 'title': "title"})
		self.result =  self.result[1:]
		return self.result


	# To initialise downloading tutorials
	def saveData(self):
		if self.result == []:
			self.getList()
		for result in self.result:
			time.sleep(1)
			seed = result['link']
			print seed
			name = "googleRes/" + seed.split("/")[-1].split(".")[0]	+ ".txt"
			self.__downloadData(seed, name)
		print "Done SucessFully..."


# Run if this file is being run as main file
if __name__ == "__main__":	
	seed =  raw_input("please type the base link : ")
	print seed
	obj = textMining(seed)
	obj.saveData()
