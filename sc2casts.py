import urllib,urllib2,re,sys,os,string,xbmcaddon,xbmcgui,xbmcplugin
		
###################################
########  Class SC2Casts  #########
###################################
				
class SC2Casts:	

	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
	__settings__ = xbmcaddon.Addon(id='plugin.video.sc2casts')
	
	# ------------------------------------- Main functions ------------------------------------- #
	
	# display the root menu
	def root(self):
		self.addCategory('recent casts', 'http://www.sc2casts.com', 'showTitles')
		self.addCategory('top casts', '', 'rootTop')
		self.addCategory('browse casts', '', 'rootBrowse')
	
	# display the top casts menu
	def rootTop(self):
		self.addCategory('top all time', 'http://www.sc2casts.com/top?all', 'showTitlesTop')
		self.addCategory('top month', 'http://www.sc2casts.com/top?month', 'showTitlesTop')
		self.addCategory('top week', 'http://sc2casts.com/top?week', 'showTitlesTop')
		self.addCategory('top 24 hours', 'http://sc2casts.com/top', 'showTitlesTop')
	
	# display the browse casts menu
	def rootBrowse(self):
		self.addCategory('browse events', '', 'browseEvents')
	
	# display the browse events menu
	def browseEvents(self):
		self.addCategory('TSL 3', 'http://sc2casts.com/event227-TSL-3', 'showTitles')

	def addCategory(self,title,url,action):
		url=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&title="+urllib.quote_plus(title)+"&action="+urllib.quote_plus(action)
		listitem=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		listitem.setInfo( type="Video", infoLabels={ "Title": title } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True)
		
	def addDirectory(self,title,url,action):
		url=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&title="+urllib.quote_plus(title)+"&action="+urllib.quote_plus(action)
		liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		liz.setInfo( type="Video", infoLabels={ "Title": title } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)
		
	def addVideo(self,title,url):
		# Check if URL is a 'fillUp' URL
		if url != 'fillUp':
			url = self.getVideoUrl(url)
		liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
		liz.setInfo( type="Video", infoLabels={ "Title": title } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

	def action(self, params):
		get = params.get
		if (get("action") == "rootTop"):
			self.rootTop()
		if (get("action") == "rootBrowse"):
			self.rootBrowse()
		if (get("action") == "browseEvents"):
			self.browseEvents()
		if (get("action") == "showTitles" or get("action") == "showTitlesTop"):
			self.showTitles(params)
		if (get("action") == "showGames"):
			self.showGames(params)
		
	def getParams(self, paramList):	
		splitParams = paramList[paramList.find('?')+1:].split('&')
		paramsFinal = {}
		for value in splitParams:
			splitParams = value.split('=')
			type = splitParams[0]
			content = splitParams[1]
			if type == 'url':
				content = urllib.unquote_plus(content)
			paramsFinal[type] = content
		return paramsFinal
			
			
	# ------------------------------------- show functions ------------------------------------- #
	
	def showTitles(self, params = {}):
		get = params.get
		req = urllib2.Request(get("url"))
		req.add_header('User-Agent', self.USERAGENT)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		if get("action") == 'showTitlesTop':
			info=re.compile('<a href="(.+?)"><b >(.+?)</b> vs <b >(.+?)</b>&nbsp;(.*?)</a>').findall(link)
		else:
			info=re.compile('<a href="(.+?)"><b >(.+?)</b> vs <b >(.+?)</b>(.*?)</a>').findall(link)
		caster=re.compile('<a href="/.+?"><span class="caster_name">(.+?)</span></a>').findall(link)
		matchup=re.compile('<span style="color:#cccccc">(.*?)</span>').findall(link)
		for i in range(len(info)):
			self.addDirectory(info[i][3] + ' - ' + matchup[i] +' ' + info[i][1] + " vs " + info[i][2] + " casted by " + caster[i],info[i][0],'showGames')
			
	def showGames(self, params = {}):
		get = params.get
		url = 'http://sc2casts.com/'+get("url")
		req = urllib2.Request(url)
		req.add_header('User-Agent', self.USERAGENT)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		matchCount = re.compile('<div id="g(.+?)"(.+?)</div></div>').findall(link)
		
		if len(matchCount) > 0:
			for i in range(len(matchCount)):
				videoContent=re.compile('<param name="movie" value="http://www.youtube.com/v/(.+?)\?.+?"></param>').findall(matchCount[i][1])
				if len(videoContent) == 0:
					self.addVideo('Game '+ str(i+1), 'fillUp')
				if len(videoContent) == 1:
					self.addVideo('Game '+ str(i+1), videoContent[0])
				if len(videoContent) > 1:
					for k in range(len(videoContent)):
						self.addVideo('Game '+ str(i+1)+', part '+ str(k+1), videoContent[k])
		else:
			videoContent=re.compile('<param name="movie" value="http://www.youtube.com/v/(.+?)\?.+?"></param>').findall(link)
			if len(videoContent) > 1:
				for n in range(len(videoContent)):
					self.addVideo('Game 1, part '+ str(n+1), videoContent[n])
			else:
				self.addVideo('Game 1', videoContent[0])
			
			
	# ------------------------------------- Data functions ------------------------------------- #
	
	def getVideoUrl(self, url):
		url = 'http://www.youtube.com/watch?v='+url+'&safeSearch=none&hl=en_us'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
			
		fmtSource = re.findall('"fmt_url_map": "([^"]+)"', link)
		fmt_url_map = urllib.unquote_plus(fmtSource[0]).split('|')
		links = {}
			
		for fmt_url in fmt_url_map:
			if (len(fmt_url) > 7):
				if (fmt_url.rfind(',') > fmt_url.rfind('&id=')):
					final_url = fmt_url[:fmt_url.rfind(',')]
					final_url = final_url.replace('\u0026','&')
					if (final_url.rfind('itag=') > 0):
						quality = final_url[final_url.rfind('itag=') + 5:]
						quality = quality[:quality.find('&')]
					else:
						quality = "5"
					links[int(quality)] = final_url.replace('\/','/')
				else :
					final_url = fmt_url
					if (final_url.rfind('itag=') > 0):
						quality = final_url[final_url.rfind('itag=') + 5:]
						quality = quality[:quality.find('&')]
					else :
						quality = "5"
					links[int(quality)] = final_url.replace('\/','/')
		
		hd_quality = int(self.__settings__.getSetting( "hd_videos" ))
		get = links.get
		
		# Select SD quality, standard
		if (get(35)):
			url = get(35)
		elif (get(34)):
			url = get(34)
		
		# Select HD quality if wanted
		if (hd_quality > 0): # <-- 720p
			if (get(22)):
				url = get(22)
		if (hd_quality > 1): # <-- 1080p
			if (get(37)):
				url = get(37)
				
		return url
		