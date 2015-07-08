import xbmc,xbmcgui,xbmcaddon                                                                                                                                                                     
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
__addon__ = xbmcaddon.Addon(id='script.homixbmc')
__cwd__         = __addon__.getAddonInfo('path')
__icon__        = __addon__.getAddonInfo('icon')

pathcwd = __cwd__
pathicon = __icon__
cwd_path = xbmc.translatePath( pathcwd )
icon_path = xbmc.translatePath( pathicon )

Xstart=__addon__.getSetting("xbmc_started")
Vstart=__addon__.getSetting("video_started")
Vstop=__addon__.getSetting("video_stopped")
Vpause=__addon__.getSetting("video_paused")
Vresume=__addon__.getSetting("video_resumed")
Astart=__addon__.getSetting("audio_started")
Astop=__addon__.getSetting("audio_stopped")
Apause=__addon__.getSetting("audio_paused")
Aresume=__addon__.getSetting("audio_resumed")

IPServer=__addon__.getSetting("IPserver")
IDServer=__addon__.getSetting("IDserver")
PortServer=__addon__.getSetting("Portserver")

device_instance_name = xbmc.getInfoLabel('System.FriendlyName')
	
if str(Vstop)=="Yes":
  	xbmc.executebuiltin('Notification(HOMIXBMC Notification,VideoPlayer STOP,5000,'+icon_path+')')
	from suds.client import Client
	import suds
		
	url = 'http://'+IPServer+':'+str(PortServer)+'/service?wsdl'
	client = Client(url)
	
	
	Alldevices=client.service.GetAllDevices(IDServer)
	for devices in Alldevices[0]:
			
		strtuple= ",".join("(%s,%s)" % tup for tup in devices).split(",")
		for it in range(len(strtuple)):
					
			if strtuple[it].find("_Name")==1:
				if str(strtuple[it+1][:-1])==str(device_instance_name):
					ValueDeviceXBMC= strtuple[it+19][:-1]
					IDDeviceXBMC= str(strtuple[it-45][:-1])
					client.service.ChangeValueOfDeviceSimple(IDServer,IDDeviceXBMC,"PlayerVStop" )