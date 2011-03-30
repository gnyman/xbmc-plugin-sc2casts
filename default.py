import sys, xbmc, xbmcplugin, xbmcaddon, sc2casts

__version__ = "0.2.1"
__plugin__ = "SC2Casts-" + __version__
__author__ = "Kristoffer Petersson"
__settings__ = xbmcaddon.Addon(id='plugin.video.sc2casts')
__language__ = __settings__.getLocalizedString

SC2Casts = sc2casts.SC2Casts()

if (not sys.argv[2]):
    SC2Casts.root()
else:
	params = SC2Casts.getParams(sys.argv[2])
	get = params.get
	if (get("action")):
		SC2Casts.action(params)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))