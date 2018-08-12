#!/usr/bin/env python

__author__ = "Satyendra Pandey"
__email__  = "pandeys@iitk.ac.in"


import urllib, os, time, sys
from bs4 import BeautifulSoup as Soup

# setting default encoding as utf-8 so encodeing problem doesn't come
reload(sys)
sys.setdefaultencoding("utf-8")


# Defining class to scrap data from tutorials point
class scrapTutorials:
	
	# To intialise the class
	def __init__(self, seed = None):
		if seed == None:
			raise Exception("Please give the initial page as seed, like to download tutorials on HTMl give seed as : https://www.tutorialspoint.com/html/html_overview.htm")
		self.seed = seed
		self.result = []
		self.__CheckDir("Tutorials")
		self.__CheckDir("Out")

	
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
		with open("Out/linkSub.csv", 'a') as temp:
			temp.write("".join(name.split("/")[-1].split(".")[0].split()) + "\t" + seed + "\n")


	# To find and preserve order from the html page
	def __tagOrder(self, tempOrders):
		arr = []
		for tempOrder in tempOrders:
			if str(tempOrder)[:3] == "<p>":
				arr.append(0)
			elif str(tempOrder)[:4] == "<h2>":
				arr.append(1)
		return arr

	
	# To write data in specific format
	def __writeOrder(self, headers, paras, order):
		temp_str = ""
		hcount = 0
		pcount = 0
		for i in range(len(order)):
			if order[i] == 0:
				temp_str += "<para> " + paras[pcount].text + " </para>\n"
				pcount += 1				
			else:
				temp_str += "<header> " + headers[hcount].text + " </header>\n"
				hcount += 1
		return temp_str


	# To save the subtitle result into text file in Tutorials directory
	def __downloadData(self, seed, name):
		try:
			temp = urllib.urlopen(seed)
			Page_Html = temp.read()
			Parsed_html = Soup(Page_Html, 'html.parser')
			Container = Parsed_html.findAll("div", {"class":"col-md-7 middle-col"})[0]
			tempOrders =  Container.findAll()	 
			paras = Container.findAll("p")
			headers = Container.findAll("h2")
			order = self.__tagOrder(tempOrders)
			temp_str = self.__writeOrder(headers, paras, order)
			if "quick_guide" not in name:			
				self.__writer(temp_str, name, seed)
		except:
			pass


	# To get the basic link to all the other portions of that given tutorial 	
	def getList(self):
		temp = urllib.urlopen(self.seed)
		Page_Html = temp.read()
		Parsed_html = Soup(Page_Html, 'html.parser')
		Container = Parsed_html.findAll("div", {"class":"col-md-2"})[0]
		main_Containers = Container.findAll("ul", {"class":"nav nav-list primary left-menu"})
		for main_Container in main_Containers:
			details = main_Container.findAll("li")
			for detail in details:	
				try:
					link = "https://www.tutorialspoint.com" + detail.findAll('a')[0]['href']			
					self.result.append({"link": link, 'title': title})
				except:
					title = detail.text
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
			name = "Tutorials/" + seed.split("/")[-1].split(".")[0]	+ ".txt"
			self.__downloadData(seed, name)
		print "Done SucessFully..."


# Run if this file is being run as main file
if __name__ == "__main__":	
	seed = raw_input("please type the base link : ")
	obj = scrapTutorials(seed)
	obj.saveData()
