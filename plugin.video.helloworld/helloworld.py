import xbmc
import xbmcaddon
 
__addon__       = xbmcaddon.Addon(id='script.homixbmc')
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

title = "Hello World"
text = "This is some text"
time = 5000  # ms
 
xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(title, text, time, __icon__))