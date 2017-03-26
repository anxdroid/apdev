# -*- coding: utf-8 -*-
import requests
import re
import sys

class EZTV:
    #url = "https://eztv.ag/myshows/837/add/"
    #url = "https://eztv.ag/myshows/92/remove/"
    
	def getIconLink(self, show_info):
		#"https://eztv.ag/ezimg/thumbs/12-monkeys-1170.jpg"
		url = "https://eztv.ag/ezimg/thumbs/"
		show = show_info[1].replace(" ", "-")
		show = show.replace("'", "")
		show = show.replace(":", "")
		show = show.replace("/", "")
		show = show.replace(".", "")
		show = show.replace("(", "")
		show = show.replace(")", "")
		show = show.replace("!", "")
		show = show.replace(",", "")
		show = show.lower()
		return url+show+"-"+show_info[0]+".jpg"

	def getTVShowInfo(self, showId, showName):
		self.login("zioanx", "resistore")
		url = "https://eztv.ag/shows/"+str(showId)+"/"+showName+"/"
		#print url
		r = self.s.get(url)
		#<a href="/shows/1342/the-expanse/" class="thread">Expanse, The</a>
		p = re.compile('<meta property="og\:description" content="([^"]+)"\/>')
		text = r.text.encode("utf-8")
		text = text.replace("<p>", "")
		text = text.replace("</p>", "")
		vals = p.findall(text)
		#print vals
		return vals

	def getMyTVShows(self):
		self.login("zioanx", "resistore")
		url = "https://eztv.ag/myshows/list/"
		r = self.s.get(url)
		#<a href="/shows/1342/the-expanse/" class="thread">Expanse, The</a>
		p = re.compile('<a href="\/shows\/(\d+)\/([^\/]+)\/"')
		vals = p.findall(str(r.text))
		shows = {}
		for val in vals:
			#print val
			info = self.getTVShowInfo(val[0], val[1])
			shows[int(val[0])] = {"url_show_name" : val[1], "show_desc" : info[0]}
		print shows
		return shows

	def addTvShow(self, showId):
		self.login("zioanx", "resistore")
		url = "https://eztv.ag/myshows/"+showId+"/add/"
		r = self.s.get(url)
		#print url       

	def getTVShows(self):
		self.login("zioanx", "resistore")
		url = "https://eztv.ag/js/search_shows1.js"
		r = self.s.get(url)
		#<option value="449">10 O'Clock Live</option>
		#<option value="(\d+)">([^<]+)<\/option>
		p = re.compile('"id"\:"(\d+)","text"\:"([^"]+)"')
		vals = p.findall(str(r.text))
		shows = {}
		for val in vals:
			shows[int(val[0])] = {"show_name": val[1], "show_img": self.getIconLink(val)}
		return shows

	def login(self, user, passwd):
		url = "https://eztv.ag/login/"
		data = {"loginname": user, "password": passwd, "submit" : "Login"}
		r = self.s.post(url, data)
		#print r.text

	def __init__(self):
		self.s = requests.session()
