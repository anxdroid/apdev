# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urlparse
import datetime
import StorageServer
from resources.lib.eztv import EZTV
import resources.lib.utils as utils

# plugin constants
__plugin__ = "plugin.video.eztv"
__author__ = "Thejedi82"

Addon = xbmcaddon.Addon(id=__plugin__)


# plugin handle
handle = int(sys.argv[1])

# Cache channels for 1 hour
cache = StorageServer.StorageServer(__plugin__, 1) # (Your plugin name, Cache time in hours)
all_tv_shows = cache.cacheFunction(EZTV().getTVShows)

#all_tv_shows = eztv.getTVShows()
# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = dict(urlparse.parse_qsl(parameters[1:]))
    return paramDict
 
def addDirectoryItem(parameters, li):
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=True)

def addLinkItem(parameters, li, url=""):
    if url == "":
        url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=False)



# UI builder functions
def show_all_tv_shows():
	my_tv_shows = eztv.getMyTVShows()
	print my_tv_shows
	thumb = "https://s-media-cache-ak0.pinimg.com/originals/96/c8/81/96c881d60407afffd3ae4c38b338cec5.jpg"
	#icon = "http://www.iconarchive.com/download/i60487/custom-icon-design/pretty-office-9/baby-boy.ico";
	for tv_show_id in my_tv_shows.keys():
		tv_show = all_tv_shows[tv_show_id]
		my_tv_show = my_tv_shows[tv_show_id]
		liStyle = xbmcgui.ListItem("[B]"+tv_show["show_name"]+"[/B]", thumbnailImage=tv_show["show_img"])
		liStyle.setInfo(type='video', infoLabels={'plot': my_tv_show["show_desc"] })
		liStyle.setProperty('IsPlayable', 'false')
		addLinkItem({"mode": "remove", "show_id" : tv_show_id, "show_name" : tv_show["show_name"]}, liStyle)
		all_tv_shows.pop(tv_show_id, None)	
	
	for tv_show_id in all_tv_shows.keys():
		tv_show = all_tv_shows[tv_show_id]
		liStyle = xbmcgui.ListItem(tv_show["show_name"], thumbnailImage=tv_show["show_img"])
		liStyle.setProperty('IsPlayable', 'false')
		addLinkItem({"mode": "add_tv_shows", "show_id" : tv_show_id, "show_name" : tv_show["show_name"]}, liStyle)
	
	xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_root_menu():
    ''' Show the plugin root menu '''
    liStyle = xbmcgui.ListItem("All TV Shows")
    addDirectoryItem({"mode": "all_tv_shows"}, liStyle)
    #liStyle = xbmcgui.ListItem("Favourites")
    #addDirectoryItem({"mode": "live_radio"}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def add_tv_show(showId, showName):
	eztv.addTvShow(showId)
	xbmcgui.Dialog().ok(__plugin__, "Added "+showName+" to favourites")
	xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

# parameter values
params = parameters_string_to_dict(sys.argv[2])

mode = str(params.get("mode", ""))
showId = str(params.get("show_id", ""))
showName = str(params.get("show_name", ""))

eztv = EZTV()
if mode == "all_tv_shows":
	show_all_tv_shows()
elif mode == "my_tv_shows":
	show_my_tv_shows()
elif mode == "add_tv_shows":
	add_tv_show(showId, showName)
	show_all_tv_shows() 
else:
	show_root_menu()

