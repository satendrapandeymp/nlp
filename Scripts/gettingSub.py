#!/usr/bin/env python

__author__ = "Satyendra Pandey"
__email__  = "pandeys@iitk.ac.in"

import urllib, re, os, time, sys, gc
from bs4 import BeautifulSoup as Soup


# setting default encoding as utf-8 so encodeing problem doesn't come
reload(sys)
sys.setdefaultencoding("utf-8")
  

class gettingSub:
	
	# To intialise the class
	def __init__(self, search_term=None, search_type=None):
		if search_term == None:
			 raise Exception('Just assign a search term with this class, For fun just try "HTML Tutorials" :p')
		if search_type == None:
			 search_type = "playlists"
		self.search_term = search_term
		self.search_type = search_type
		self.result = []
		self.play_result = []
		self.url = "http://www.youtube.com/results?"
		self.__CheckDir("Results")
		self.__CheckDir("Out")
		if search_type == "playlists":
			self.url += "sp=EgIQA0IECAESAA%253D%253D&"
		else:
			self.__CheckDir("Results/" + search_term)
			self.url += "sp=EgIQAQ%253D%253D&"


	# To make a directory if that is not already there
	def __CheckDir(self, Name):
		if not os.path.exists(Name):
			os.mkdir(Name)


	# To save data to inspect locally
	def __inspect(self, html_content):
		with open('temp.html', 'w') as temp_writer:
			temp_writer.write(html_content)
		print "Please open the temp.html file to see if there is any error..."


	# To parse data to get videos/tutorials of a search result
	def __ParsedData(self, html_content):
		Parsed_html = Soup(html_content, "html.parser")
		Container = Parsed_html.findAll("div", {"id":"results"})[0]
		titles = Container.findAll("h3")
		for title in titles:
			try:
				url =  title.findAll("a")[0]
				link = "https://www.youtube.com" + url['href']	
				title = url.text
				re.sub(r'\W+', '', title)
				if "/watch?v" in link:
					self.result.append({"title": title, "url": link})
			except:
				pass


	# To parse data to get videos of a tutorials
	def __ScrapPlaylist(self, details):
		playlist = details['url']
		html_content = urllib.urlopen(playlist)
		Parsed_html = Soup(html_content.read(), "html.parser")
		Container = Parsed_html.findAll("div", {"class":"playlist-videos-container yt-scrollbar-dark yt-scrollbar"})[0]
		links = Container.findAll("a")
		for link in links:
			vtitle = link.findAll("h4")[0].text
			re.sub(r'\W+', '', vtitle)
			temp = {"link": "https://www.youtube.com" + link['href'], "vtitle": vtitle}
			temp.update(details)
			self.play_result.append(temp)

	
	# to initiate search for playlist or video
	def get_list(self):                                                                                                                            
		query_string = urllib.urlencode({"search_query" : self.search_term})
		html_content = urllib.urlopen(self.url + query_string)
		html_content = html_content.read()
		self.__ParsedData(html_content)
		return self.result

	
	# To get all the videos from that search
	def get_videos(self, num=None):
		if self.result == []:
			self.get_list()
		if self.play_result != []:
			return self.play_result			
		if self.search_type != "playlists":
			return self.result
		if num == None:
			num = len(self.result)
		for i in range(1,num):
			playlist = self.result[i]
			time.sleep(2)
			self.__ScrapPlaylist(playlist)
		return self.play_result


	# To process subtitle
	def __process_sub(self, link, name):
		try:
			temp = urllib.urlopen(link)
			Page_Html = temp.read()
			Parsed_html = Soup(Page_Html, "html.parser")
			Container = Parsed_html.findAll("div", {"class":"well"})[0]
			text = Container.contents[3]
			with open(name, "w") as temp:
				temp.write(str(text))
			with open("Out/linkSub.csv", 'a') as temp:
				temp.write("".join(name.split("/")[-1].split(".")[0].split()) + "\t" + link.split("id=")[1].split("&")[0] + "\n")
		except:
			self.__inspect(Page_Html)
		

	# To download all the subtitles	
	def Get_subtitle(self):
		
		if self.result == []:
			self.get_list()
		if self.play_result == [] and self.search_type == "playlists":
			_ = self.get_videos()
		
		temp_data = self.result
		if self.search_type == "playlists":
			temp_data = self.play_result
	
		for temp_link in temp_data:
			
			
			if self.search_type != "playlists":
				vid = temp_link['url'][32:43]
				name = "\\".join(temp_link['title'].split("/"))
				name = "Results/{0}/{1}.{2}.txt".format(self.search_term, name, vid)
			else:
				vid = temp_link['link'][32:43]
				name = "\\".join(temp_link['vtitle'].split("/"))
				fname = "\\".join(temp_link['title'].split("/"))
				name = "Results/{0}/{1}.{2}.txt".format(fname, name, vid)
				self.__CheckDir("Results/" + fname)

			print "Done with ?v=" + vid
			link = "http://diycaptions.com/php/get-automatic-captions-as-txt.php?id={0}&language=asr".format(vid)
			time.sleep(1)
			link = self.__process_sub(link, name)



if __name__ == "__main__":

	title = raw_input("Please type the search keywords : ")
	obj = gettingSub(title, "Video")
	print obj.Get_subtitle()

