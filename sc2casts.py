import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,os,xbmc
		
###################################
########  Class SC2Casts  #########
###################################
				
class SC2Casts:	
		
	def categories(self):
		self.addDir('recent casts','http://www.sc2casts.com',2,'','')
		
	def addLink(self,name,url,iconimage,duration):
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name , "Duration": duration } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		
	def addDir(self,name,url,mode,iconimage,duration):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&duration="+urllib.quote_plus(duration)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		
	def index(self,url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		info=re.compile('<h2><a href="(.+?)"><b >(.+?)</b> vs <b >(.+?)</b>').findall(link)
		caster=re.compile('<a href="/.+?"><span class="caster_name">(.+?)</span></a>').findall(link)
		for i in range(len(info)):
			self.addDir(info[i][1] + " vs " + info[i][2] + " casted by " + caster[i],info[i][0],3,'','')
			
	def videolinks(self,url):
		url = 'http://sc2casts.com/'+url	
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		info=re.compile('<param name="movie" value="http://www.youtube.com/v/(.+?)?fs=1&amp;hl=en_US"></param>').findall(link)
		
		url = 'http://www.youtube.com/watch?v='+info[0]+'&safeSearch=none&hl=en_us'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
			
		fmtSource = re.findall('"fmt_url_map": "([^"]+)"', link);
		fmt_url_map = urllib.unquote_plus(fmtSource[0]).split('|')
		links = {};
			
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
					
		test = links.items()
		self.addLink('Test',test[0][1],'','')
		
	def get_params(self):
			param=[]
			paramstring=sys.argv[2]
			if len(paramstring)>=2:
					params=sys.argv[2]
					cleanedparams=params.replace('?','')
					if (params[len(params)-1]=='/'):
							params=params[0:len(params)-2]
					pairsofparams=cleanedparams.split('&')
					param={}
					for i in range(len(pairsofparams)):
							splitparams={}
							splitparams=pairsofparams[i].split('=')
							if (len(splitparams))==2:
									param[splitparams[0]]=splitparams[1]
									
			return param