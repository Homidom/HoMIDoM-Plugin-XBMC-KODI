# -*- coding: utf-8 -*-
import sys  

#reload(sys)  
#sys.setdefaultencoding('utf8')

import os, re, socket, urllib

import xbmc, xbmcgui, xbmcaddon

import time

from PIL import Image
import PIL.Image
import base64


# plugin constants
#create an add on instation and store the reference
__addon__       = xbmcaddon.Addon()

#store some handy constants

__addonname__   = __addon__.getAddonInfo('name')
__addonid__     = __addon__.getAddonInfo('id')
__author__      = __addon__.getAddonInfo('author')
__version__     = __addon__.getAddonInfo('version')
__cwd__         = __addon__.getAddonInfo('path')
__language__    = __addon__.getLocalizedString
__icon__        = __addon__.getAddonInfo('icon')

__useragent__ = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.0.1) Gecko/2008070208 Firefox/7.0"

path = __cwd__ 
cwd_path = xbmc.translatePath( path )

__settings__ = xbmcaddon.Addon(__addonid__)

IPServer=__settings__.getSetting("IPserver")
IDServer=__settings__.getSetting("IDserver")
PortServer=__settings__.getSetting("Portserver")



ACTION_MOVE_LEFT 							= 1	
ACTION_MOVE_RIGHT							= 2
ACTION_MOVE_UP								= 3
ACTION_MOVE_DOWN							= 4
ACTION_PAGE_UP								= 5
ACTION_PAGE_DOWN							= 6
ACTION_SELECT_ITEM							= 7
ACTION_HIGHLIGHT_ITEM						= 8
ACTION_PARENT_DIR							= 9
ACTION_PREVIOUS_MENU						= 10
ACTION_SHOW_INFO							= 11
KEY_BUTTON_BACK = 275
KEY_KEYBOARD_ESC = 61448 
ACTION_PAUSE								= 12
ACTION_STOP									= 13
ACTION_NEXT_ITEM							= 14
ACTION_PREV_ITEM							= 15
		
		
class HomidomW(xbmcgui.WindowXML):
  
 
  def __new__(cls):
        return super(HomidomW, cls).__new__(cls, 'script-Homidom-Menu.xml', cwd_path)

  def __init__(self):
	super(HomidomW, self).__init__()
	

  def onInit(self):
		
	self.getControl(88455).setVisible(False)
	self.getControl(88655).setVisible(False)
	self.getControl(88650).setVisible(False)
	self.getControl(99955).setVisible(False)
	self.getControl(99855).setVisible(False)
	self.getControl(88156).setVisible(False)
	self.getControl(99655).setLabel("noupdated")
	
	#nbrlistzonereel=self.getListSize()
	#if nbrlistzonereel !=0:
	self.clearList()
	
	from suds.client import Client
	import suds
	
	
	url = 'http://'+IPServer+':'+str(PortServer)+'/service?wsdl'
	print str(url)
	client = Client(url)

		
	print "**************************************"
	print "*****         HOMIDOM            *****"
	print "**************************************"

	print "il est " + client.service.GetTime ()+ " sur HoMiDom"
	print "vous etes situé a "+ str(client.service.GetLatitude ()) + " degrés de latitude et à "+ str(client.service.GetLongitude ())+ " degrés de longitude"

	print
	print
	resultuser=client.service.GetAllUsers (IDServer)

	nbrusers=len(resultuser[0])
	print "avec un nombre total de " + str(nbrusers)+" utilisateurs pour HoMiDoM"
	print
	i=0
	while i < nbrusers:
		print "nom du " +str(i+1)+" " +"utilisateur :" +" "+ resultuser[0][i][4]
		i = i+1

	print
	print
	resultzone=client.service.GetAllZones (IDServer)
	
	nbrzones=len(resultzone[0])
	print "avec un nombre total de " + str(nbrzones)+" zones pour HoMiDoM"
	print
	
	checkedList1=[]
	checkzonebool=True
	
	i=0
	while i < nbrzones:
		print "nom de la zone " +str(i+1)+" " +" :" +" "+ resultzone[0][i][4]
		
		checkedList1.append(resultzone[0][i][4])
		checklist1 = set(checkedList1)
		
		#print "MACRO"
		#print len(client.service.GetMacroInZone(IDServer,"b3773cba-2342-49f8-be9d-1b5aa24abe49"))
		
		resultdevicebyzone=client.service.GetDeviceInZone(IDServer,resultzone[0][i][1])
		print "id de la zone" 
		print "nom de la zone " +str(i+1)+" " +" :" +" "+ resultzone[0][i][4] + "  et ID : "+resultzone[0][i][1]
	
		
		
		if len(resultdevicebyzone)>=1:
			listdevice=[]
			listactiondevice=[]
			listactiondeviceB=[]
			listactiondeviceC=[]
			listnbractionr=[]
			indexaction2=[0]
			listdeviceaction=[]
			listactiondeviceA=[]
			listactiondeviceAVerif=[]
			listactiondeviceP=[]
			listactiondevicePVerif=[]
			strlistaction=[]
			listnamesorted=[]
			listididevice=[]
			listdeviceid=[]
			listdeviceidok=[]
			listdeviceidstate=[]
			liststrdevicename=[]
			listdeviceaction4action=[]
			listtypeidevice=[]
			listtypedevices=[]
			
			listididevice2=[]
			
			
			for idevice in resultdevicebyzone[0]:
				print idevice
				listididevice2.append(idevice)
			
			for iddevice2 in listididevice2:
				devicebyid = client.service.ReturnDeviceByID(IDServer,iddevice2)
				nbrtest=0
				
				##print ",".join("(%s,%s)" % tup for tup in devicebyid).split(",")
				
				strtuple= ",".join("(%s,%s)" % tup for tup in devicebyid).split(",")
							
				if any(".Parametre" in s for s in strtuple):
						for it in range(len(strtuple)):
							
							if strtuple[it].find("_Name")==1:
								listdevice.append(strtuple[it+1][:-1])
													
							if strtuple[it].find("_DriverI")==1:
								finaction=it
								
							
							if strtuple[it].find("_DeviceAction")==1:
								debutaction=it
								
							if strtuple[it].find("_ID")==1:
								listididevice.append(strtuple[it+1][:-1])
									
							
							if strtuple[it].find("_Type")==1:
								listtypeidevice.append(strtuple[it+1][:-1])
							
						nbractiontuple=0
						for iistrtuple in range (debutaction,finaction):
							if strtuple[iistrtuple].count("(DeviceAction){")!=0:
								nbractiontuple=nbractiontuple+1
											
						listnbractionr.append(nbractiontuple)
							
				else:		
								
					for it in range(len(strtuple)):
						
						if strtuple[it].find("_Name")==1:
							listdevice.append(strtuple[it+1][:-1])
							
						if strtuple[it].find("_DriverI")==1:
							finaction=it.encode('utf-8')
						
						if strtuple[it].find("_DeviceAction")==1:
							debutaction=it.encode('utf-8')
							
						if strtuple[it].find("_ID")==1:
							listididevice.append(strtuple[it+1][:-1])
								
						if strtuple[it].find("_Type")==1:
							listtypeidevice.append(strtuple[it+1][:-1])
						
					listnbractionr.append(finaction- debutaction-2)
				
				for ita in range(finaction- debutaction):
					
					for ituple in str(strtuple[debutaction+ita]).split("DeviceAction"):
						lst=ituple.split()
												   
						if len(lst)>3:
							
							listactiondevice.append(",".join(lst).replace(", '","").replace("'}']","").replace("'","").replace("){,","").replace(",}","").replace(",","").replace("(ArrayOf",""))
							
							if any(".Parametre" in s for s in lst):
								
								listactiondevice.pop()
								
								ajout= ",".join(listactiondevice).replace("']","")+",".join(lst).replace(", '","").replace("'}']","").replace("'","").replace("){,","").replace(",}","").replace(",","").replace(".Parametre","")
								
								listactiondevice=[]
								listactiondevice= ajout.split(",")
			
			nbrlistzonereel=self.getListSize()
			if checkzonebool==True:
				if nbrlistzonereel !=0:
					self.clearList()
			
			listzonesi = xbmcgui.ListItem(resultzone[0][i][4]+"  ("+str(len(listdevice))+")", str(i), '', '','')
			self.addItem(listzonesi)
			
			checkzonebool=False
				
			listname=[]
			listaction2=[]
			listactionr=[]
			inamenbr=0
			iactionnbr=0
			for iname in listdevice:
				listname.append(iname.encode('utf-8'))
				inamenbr=inamenbr+1
			
			for iaction in listactiondevice:
				listactionr.append(iaction)
				iactionnbr=iactionnbr+1
			
			listaction=listactionr[::1]
			
			for q, a in zip(listname, listnbractionr):
				
				print "zone"+str(i+1)+" : "+resultzone[0][i][4] +" avec comme nombre device "+" "+str(len(listdevice))+" pour le device :"'{0}'.format(q, a)+" : "+ str('{1}'.format(q, a)) +" actions associees"		
				listdeviceaction.append("  "+resultzone[0][i][4]+"  "+'{0}'.format(q, a))
				
				indexaction2.append(int('{1}'.format(q, a)))
				
				total = 0
				for item in range(len(indexaction2)):
					total += indexaction2[item]
				
				indexaction= listdevice.index('{0}'.format(q, a))
				
				for inameid in listdevice:
					listdeviceid.append(inameid+" %id:"+listididevice[listdevice.index(inameid)]+"  Type:"+listtypeidevice[listdevice.index(inameid)] )
				for element in listdeviceid:
					if element not in listdeviceidok:
						listdeviceidok.append(element)
				
				for elementid in listdeviceidok:
					if elementid.find('{0}'.format(q, a))!=-1:
						
						iddevice =elementid[elementid.index("%id")+4:elementid.index("Type")].strip()
						
						print "----->  nom device  "+str(listdeviceidok.index(elementid)+1) +" de la zone"+"  "+str(i+1)+"  "+resultzone[0][i][4]+"  "+" " +" :" +" "+'{0}'.format(q, a)+"  ID : "+iddevice
						resultdeviceState=client.service.ReturnDeviceByID(IDServer, iddevice)
						strtupleid= ",".join("(%s,%s)" % tup for tup in resultdeviceState).split(",")
						
						for idstrtupleid in range (len(strtupleid)):
							if strtupleid[idstrtupleid].find("_Enable")!=-1:
								statedevice=strtupleid[idstrtupleid+1][:-1]
								print "------> Etat :  "+statedevice
							if strtupleid[idstrtupleid].find("(_Description")!=-1:
								descdevice= strtupleid[idstrtupleid+1][:-1].encode("utf-8").replace("é","e%%").replace("è","e$$").replace("à","a%%") 
								print "------> Description :  "+descdevice 
							if strtupleid[idstrtupleid].find("_Value")!=-1:
								
								if strtupleid[idstrtupleid]=="(_Value":
									if strtupleid[idstrtupleid+1][:-1]!="None":
										valuedevice= strtupleid[idstrtupleid+1][:-1]
										print "------> Valeur :  "+str(valuedevice).encode("utf-8")
									if strtupleid[idstrtupleid+1][:-1]=="None":
										valuedevice= "None"
										print "------> Valeur :  "+"None"
										
						listdeviceidstate.append(elementid+"  Etat : "+statedevice+"  Desc : "+descdevice+"  Valeur : "+valuedevice)
						
						
				sumprec = 0
				for item in range(indexaction-1):
					sumprec += listnbractionr[item]
								
				sum = 0
				for item in range(indexaction):
					sum += listnbractionr[item]
				
				if sumprec==0 and sum==0:
					
					for item in range(int('{1}'.format(q, a))):
						listdeviceaction.append( listactiondevice[item][listactiondevice[item].index("Nom")+5:listactiondevice[item].index("Parametres")-1])
						listdeviceaction4action.append("  "+resultzone[0][i][4]+"  "+'{0}'.format(q, a) +" ..."+ listactiondevice[item])
					
				elif sumprec==0 :
					
					for item in range(sum,total):
						listdeviceaction.append( listactiondevice[item][listactiondevice[item].index("Nom")+5:listactiondevice[item].index("Parametres")-1])
						listdeviceaction4action.append("  "+resultzone[0][i][4]+"  "+'{0}'.format(q, a) +" ..."+ listactiondevice[item])
									
				elif int('{1}'.format(q, a))==total-sumprec-1:
					
					for item in range(sumprec+1,total):
						
						if listactiondevice[item].find("Parametres=None")!=1:
						
							listdeviceaction.append(listactiondevice[item][listactiondevice[item].index("Nom")+5:listactiondevice[item].index("Parametres")-1])
							listdeviceaction4action.append("  "+resultzone[0][i][4]+"  "+'{0}'.format(q, a) +" ..."+ listactiondevice[item])
						
			
				elif int('{1}'.format(q, a))!=total-sumprec-1:
									
					if (len(listdeviceaction)-1)-(total-sum)+2!=len(listdeviceaction):
					
						for item in range(sum,total):
							
							listdeviceaction.append(listactiondevice[item][listactiondevice[item].index("Nom")+5:listactiondevice[item].index("Parametres")-1])
							listdeviceaction4action.append("  "+resultzone[0][i][4]+"  "+'{0}'.format(q, a) +" ..."+ listactiondevice[item])
					else:
					
						listdeviceaction.append(listactiondevice[sum][listactiondevice[sum].index("Nom")+5:listactiondevice[sum].index("Parametres")-1])
						listdeviceaction4action.append("  "+resultzone[0][i][4]+"  "+'{0}'.format(q, a) +" ..."+ listactiondevice[item])

			
			strlistname ='...'.join(listname)
			strllistdeviceidstate= str(listdeviceidstate)
			
			list = self.getControl(88750)
			listitemdevice = xbmcgui.ListItem(strlistname, strllistdeviceidstate, '', '','')
			list.addItem(listitemdevice)
			strlistaction="...".join(listdeviceaction)
			strlistdeviceaction4action=str(listdeviceaction4action)
			list = self.getControl(88550)
			listitemdeviceaction = xbmcgui.ListItem(strlistaction, strlistdeviceaction4action)
			list.addItem(listitemdeviceaction)
		
		resultimage=client.service.GetByteFromImage(resultzone[0][i][2])
		if resultimage!= None:
			fh = open(cwd_path +"/resources/imagesdw/"+ resultzone[0][i][4]+".png", "wb")
			fh.write(resultimage.decode('base64'))
			fh.close()	
			img = Image.open(cwd_path +"/resources/imagesdw/"+ resultzone[0][i][4]+".png")
		i = i+1
		
  def onClick(self, controlID):
	listdevicetype=[]
	
	if (controlID == 50):
        
		self.getControl(99656).setLabel("")
		self.getControl(88451).setLabel("Action")
		self.getControl(99855).setVisible(False)
		time.sleep(0.45)
		self.getControl(88650).setVisible(False)
		self.getControl(88655).setVisible(False)
		self.getControl(99955).setVisible(False)
		if self.getControl(88455).getPosition()==[0, 0]:
			time.sleep(0.25)
			self.getControl(88455).setVisible(False)
		deviceselected=""
		self.getControl(88847).setLabel("")
		self.getControl(88440).setLabel("")
		self.getControl(99755).setVisible(False)
		time.sleep(0.3)
		self.getControl(88355).setVisible(False)
		self.getControl(88855).setVisible(False)
		self.getControl(88850).reset()
		self.getControl(88650).reset()
		ctl=self.getControl(50)
		indexlist=int(xbmc.getInfoLabel("Listitem.Label2"))
		indexlistprec=indexlist#-1
		listlabel=xbmc.getInfoLabel("Listitem.Label")
		self.getControl(88655).setVisible(False)
		self.getControl(88650).reset()
		
		if indexlist==0 and listlabel!=".." and listlabel.find("(")==-1:
			print "media insered"
			self.message("The media  named  "+ listlabel +" has been insered")
			HomidomW.onInit(self)
		if indexlist==0 and listlabel!=".." and listlabel.find(":)")!=-1:
			print "media insered"
			self.message("The media  named  "+ listlabel +" has been insered")
			HomidomW.onInit(self)
		
		
		
		
		
		if indexlist==0 and listlabel=="..":
			print "index   0"
			print listlabel
			self.getControl(88850).reset()
			self.getControl(88650).reset()
			self.getControl(88846).setLabel("")
			self.getControl(88845).setLabel("")
			self.getControl(99755).setVisible(False)
			self.getControl(99855).setVisible(False)
			time.sleep(0.30)
			self.getControl(88455).setVisible(False)
			
		else:
			
			self.getControl(99855).setVisible(False)
			self.getControl(88845).setLabel("  "+listlabel[:listlabel.index("(")-1])
			self.getControl(88750).selectItem(indexlistprec)
			self.getControl(88550).selectItem(indexlistprec)
			time.sleep(0.5)
			devices=self.getControl(88750).getSelectedItem().getLabel()
			listtypedevices=self.getControl(88750).getSelectedItem().getLabel2().split(",")
			
			for itypedevice in listtypedevices:
				listdevicetype.append(itypedevice[itypedevice.index("Type")+5:-1].replace("'","").replace("]","").strip())
					
			idevices=devices.split("...")
			
			for idevicesnbr in idevices:
				
				devicetype=listdevicetype[idevices.index(idevicesnbr)][:listdevicetype[idevices.index(idevicesnbr)].index("Etat")].strip()
				devicestate= listdevicetype[idevices.index(idevicesnbr)][listdevicetype[idevices.index(idevicesnbr)].index("Etat :")+7:listdevicetype[idevices.index(idevicesnbr)].index("Desc :")].strip()
				devicedesc= listdevicetype[idevices.index(idevicesnbr)][listdevicetype[idevices.index(idevicesnbr)].index("Desc :")+7:listdevicetype[idevices.index(idevicesnbr)].index("Valeur :")].strip().replace("e%%","é").replace("e$$","è").replace("a%%","à") 
				devicevaleur= listdevicetype[idevices.index(idevicesnbr)][listdevicetype[idevices.index(idevicesnbr)].index("Valeur :")+9:].strip()
				if devicestate=="False":
					devicetypeimage=cwd_path +"/resources/DeviceType/"+devicetype+".png"
				else :
					devicetypeimage=cwd_path +"/resources/DeviceType/"+devicetype+"-ON.png"
				
				statedesc=devicestate+"..."+devicedesc+"---"+devicevaleur
				listitem = xbmcgui.ListItem(idevicesnbr, statedesc, devicetypeimage)
				self.getControl(88850).addItem(listitem)
				listitem.setProperty("imagestatedevice", devicetypeimage)
			
			self.getControl(88846).setLabel("")
			#self.getControl(88846).setLabel( " - "+"  "+self.getControl(88850).getSelectedItem().getLabel())
			self.getControl(99901).setImage(cwd_path +"/resources/imagesdw/"+listlabel[:listlabel.index("(")-1].strip()+".png")
			self.getControl(98888).setVisible(False)
			self.getControl(98889).setVisible(False)
			time.sleep(0.3)
			self.getControl(88455).setVisible(False)
			ctl.selectItem(indexlistprec)
			ctl.selectItem(indexlist)
	

		if self.getFocusId(50) and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()!= " - "+"  "+"$" and self.getControl(88847).getLabel()!= " - "+"  "+"TEST":
				self.getControl(88845).setVisible(True)
				listlabel=xbmc.getInfoLabel("Listitem.Label")
				self.getControl(88845).setLabel("  "+listlabel[:listlabel.index("(")-1])
				self.getControl(99901).setImage(cwd_path +"/resources/imagesdw/"+listlabel[:listlabel.index("(")-1].strip()+".png")
				self.getControl(88855).setVisible(True)
				self.getControl(88355).setVisible(False)
				self.getControl(99755).setVisible(True)
				self.getControl(88355).setVisible(True)
				self.getControl(88847).setLabel()== " - "+"  "+"$$"
				self.getControl(88847).setVisible(False)
			
	if (controlID == 88850):
		
		self.getControl(99955).setVisible(False)
		self.getControl(99855).setVisible(False)	
		self.getControl(88650).setVisible(False)
				
		self.getControl(88650).reset()
		zone= self.getControl(88845).getLabel()
		device= self.getControl(88846).getLabel()
		zone=zone.strip()	
		indexlist=int(xbmc.getInfoLabel("Container.Position"))
		indexlistprec=indexlist-1
		listlabel=xbmc.getInfoLabel("Listitem.Label")
		print "zone selected   :  "+listlabel
		print "deviceselected  :  "+self.getControl(88850).getSelectedItem().getLabel().strip()
		statedescdevice=self.getControl(88850).getSelectedItem().getLabel2()
		etatdevice=statedescdevice[:statedescdevice.index("...")].strip()
		descdevice=statedescdevice[statedescdevice.index("...")+3:statedescdevice.index("---")].strip()
		valeurdevice=statedescdevice[statedescdevice.index("---")+3:].strip()
		pos=self.getControl(88850).getSelectedPosition()
		self.getControl(88850).getSelectedItem().select(True)
		deviceselected=self.getControl(88850).getSelectedItem().getLabel().strip()
		strdevicesaction=self.getControl(88550).getSelectedItem().getLabel()
		ideviceselected=strdevicesaction.index(deviceselected)
		strdeviceaction=strdevicesaction.split(zone)[pos+1]
		imagedevice=self.getControl(88850).getSelectedItem().getProperty("imagestatedevice")
		lstdeviceaction= strdeviceaction.replace(deviceselected,"verif").replace(" ","verif")[1:].split("...")
		
		for iok3 in range (1,len(lstdeviceaction)):
			if lstdeviceaction[iok3]!="verifverif":
				self.getControl(88650).addItem(lstdeviceaction[iok3])
							
		self.getControl(88847).setLabel( " - "+"  "+"TEST")
		positionI=self.getControl(88850).selectItem(pos)
		
		if self.getControl(88440).getLabel()=="":
			self.getControl(88847).setLabel( " - "+"  "+"$")
			self.getControl(88847).setVisible(False)
			self.getControl(88846).setLabel( " - "+"  "+self.getControl(88850).getSelectedItem().getLabel())
			self.getControl(88451).setLabel("Action")
			self.getControl(99955).setVisible(True)
			if self.getControl(88455).getPosition()!=[0, 0]:
				time.sleep(0.1)
				self.getControl(88455).setVisible(True)
				
			
		if deviceselected==self.getControl(88440).getLabel():
			self.getControl(99656).setLabel(str(self.getControl(88850).getSelectedPosition()))
			self.getControl(88847).setLabel( " - "+"  "+"$")
			self.getControl(88847).setVisible(False)
			self.getControl(88846).setLabel( " - "+"  "+self.getControl(88850).getSelectedItem().getLabel())
			self.getControl(88451).setLabel("Action")
			self.getControl(99955).setVisible(False)
			self.getControl(88850).getSelectedItem().select(False)
			if self.getControl(88455).getPosition()==[0, 0]:
				time.sleep(0.25)
				self.getControl(88455).setVisible(False)
		
			if self.getControl(88850).size()==1:
				time.sleep(0.45)
				self.getControl(99955).setVisible(True)
				time.sleep(0.1)
				self.getControl(88455).setVisible(True)
				
		if deviceselected !=self.getControl(88440).getLabel():
			if self.getControl(99656).getLabel()!= '':
			
				if self.getControl(88850).getListItem(int(self.getControl(99656).getLabel())).getLabel() != deviceselected:
					self.getControl(88850).getListItem(int(self.getControl(99656).getLabel())).select(False)
			
			self.getControl(99656).setLabel(str(self.getControl(88850).getSelectedPosition()))
			self.getControl(88846).setLabel( " - "+"  "+self.getControl(88850).getSelectedItem().getLabel())
			self.getControl(88847).setLabel( " - "+"  "+"$")
			self.getControl(88847).setVisible(False)
			self.getControl(88451).setLabel("Action")
			self.getControl(99955).setVisible(False)
			if self.getControl(88455).getPosition()==[0, 0]:
				time.sleep(0.25)
				self.getControl(88455).setVisible(False)
			time.sleep(0.35)
			self.getControl(88850).selectItem(pos)
			self.getControl(99955).setVisible(True)
			time.sleep(0.1)
			self.getControl(88455).setVisible(True)
			self.getControl(88655).setVisible(False)
		
		self.getControl(88440).setLabel(deviceselected)
		if descdevice!="None":
			self.getControl(88441).setLabel(descdevice)
		if descdevice=="None":
			self.getControl(88441).setLabel("")
		
		self.getControl(88443).setLabel(etatdevice)
		self.getControl(88445).setLabel(valeurdevice)
		self.getControl(88446).setImage(imagedevice)
		
	if (controlID == 88451):
	
		if self.getControl(88451).getLabel()=="...":
			self.getControl(99855).setVisible(False)
			self.getControl(88451).setLabel("Action")
			self.getControl(88650).setVisible(False)
			time.sleep(0.35)
			self.getControl(88655).setVisible(False)
		else:
			self.getControl(88650).setVisible(True)
			self.getControl(88655).setVisible(True)
			self.getControl(88451).setLabel("...")
			self.getControl(99855).setVisible(True)
			self.getFocusId(88650)
	
	if (controlID == 88255):
		if self.getControl(99655).getLabel()== "noupdated":
			self.getControl(88156).setVisible(True)
			self.getControl(99655).setLabel("updated")
		else:
			self.getControl(88156).setVisible(False)
			self.getControl(99655).setLabel("noupdated")
	
	if (controlID == 88650):
		
		lstactionparam=[]
		lstactionparamok=[]
		lstactionparamok2=[]
		lstactionparamok3=[]
		lstactionparamok4=[]
		action=self.getControl(88650).getSelectedItem().getLabel()
		deviceids= self.getControl(88750).getSelectedItem().getLabel2().split(",")
		deviceselected=self.getControl(88440).getLabel()
		
		for deviceid in deviceids:
			if deviceid.find(deviceselected)!=-1 :
				iddevice= deviceid[deviceid.index("id:")+3:deviceid.index("Type:")].replace("'","").strip()
		
		actionparams= self.getControl(88550).getSelectedItem().getLabel2().split(",")
		
		for actionparam in actionparams:
			if actionparam.find(self.getControl(88845).getLabel())!=-1 :
				if actionparam.find(self.getControl(88440).getLabel())!=-1 :
					if actionparam.find(self.getControl(88650).getSelectedItem().getLabel())!=-1 :
						actionparamok=actionparam.replace("u'","").replace("'","").strip()
						paramparam=actionparamok[actionparamok.index("Parametres")+11:]
						
		from suds.client import Client
		import suds
		
		url = 'http://'+IPServer+':'+str(PortServer)+'/service?wsdl'
		client = Client(url)
		
		if paramparam!="None":
			keyboard = xbmc.Keyboard("", "Parameter for the action")
			keyboard.doModal()
			if ( keyboard.isConfirmed() ):
				param1=keyboard.getText()
		else:
			param1=""
		
		
		
		requestDeviceActionSimple = client.factory.create('ns1:DeviceActionSimple')
		requestDeviceActionSimple.Nom=action
		requestDeviceActionSimple.Param1= param1
        	
		client.service.ExecuteDeviceCommandSimple(IDServer,iddevice,requestDeviceActionSimple )
				
		resultDevicebyId=client.service.ReturnDeviceByID(IDServer, iddevice)
		
		
		resultDevicebyIdtuple= ",".join("(%s,%s)" % tup for tup in resultDevicebyId).split(",")
		for resultDevicebyIdelement in range (len(resultDevicebyIdtuple)):
			
			if resultDevicebyIdtuple[resultDevicebyIdelement].find("_Name")!=-1:
				namedeviceaction=resultDevicebyIdtuple[resultDevicebyIdelement+1][:-1]
				print "------> Name device de l' action:  "+namedeviceaction
			
			if resultDevicebyIdtuple[resultDevicebyIdelement].find("_Type")!=-1:
				typedeviceaction=resultDevicebyIdtuple[resultDevicebyIdelement+1][:-1]
				print "------> Type device de l' action:  "+typedeviceaction
			
			if resultDevicebyIdtuple[resultDevicebyIdelement].find("_Enable")!=-1:
				statedeviceaction=resultDevicebyIdtuple[resultDevicebyIdelement+1][:-1]
				print "------> Etat apres action:  "+statedeviceaction
			if resultDevicebyIdtuple[resultDevicebyIdelement].find("_Value")!=-1:
				if resultDevicebyIdtuple[resultDevicebyIdelement]=="(_Value":
					if resultDevicebyIdtuple[resultDevicebyIdelement+1][:-1]!="None":
						valuedeviceaction= resultDevicebyIdtuple[resultDevicebyIdelement+1][:-1]
						print "------> Valeur apres action :  "+str(valuedeviceaction).encode("utf-8")
		
		if statedeviceaction=="False":
			imagedevicetypeaction=cwd_path +"/resources/DeviceType/"+typedeviceaction+".png"
		else :
			imagedevicetypeaction=cwd_path +"/resources/DeviceType/"+typedeviceaction+"-ON.png"
			
		self.getControl(88443).setLabel(statedeviceaction)
		self.getControl(88445).setLabel(valuedeviceaction)
		self.getControl(88446).setImage(imagedevicetypeaction)
		indexselecteddeviceaction= self.getControl(88750).getSelectedItem().getLabel().split("...").index(namedeviceaction)
		print indexselecteddeviceaction
		self.getControl(88850).selectItem(indexselecteddeviceaction)
		self.getControl(88850).getListItem(indexselecteddeviceaction).setIconImage(imagedevicetypeaction)
		self.getControl(88850).getListItem(indexselecteddeviceaction).select(False)
  def onAction(self, action):
	if (action == ACTION_PREVIOUS_MENU ):
		self.close()
	buttonCode =  action.getButtonCode()
	actionID   =  action.getId()
	if (buttonCode == KEY_BUTTON_BACK or buttonCode == KEY_KEYBOARD_ESC):
		self.close()
	
	if ((buttonCode == 61569 or buttonCode==61568)):
		
		if self.getFocusId(50) and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()!= " - "+"  "+"$" and self.getControl(88847).getLabel()!= " - "+"  "+"TEST":
			self.onClick(50)
			self.getControl(88845).setVisible(True)
			listlabel=xbmc.getInfoLabel("Listitem.Label")
			self.getControl(88845).setLabel("  "+listlabel[:listlabel.index("(")-1])
			self.getControl(99901).setImage(cwd_path +"/resources/imagesdw/"+listlabel[:listlabel.index("(")-1].strip()+".png")
			self.getControl(88855).setVisible(True)
			self.getControl(88355).setVisible(False)
			self.getControl(99755).setVisible(True)
			self.getControl(88355).setVisible(True)
			self.getControl(88847).setLabel()== " - "+"  "+"$$"
			self.getControl(88847).setVisible(False)
		
		if self.getFocusId(88850) and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()!= " - "+"  "+"TEST":
			
			self.getControl(88846).setLabel( " - "+"  "+self.getControl(88850).getSelectedItem().getLabel())
			self.getControl(88451).setLabel("Action")
			self.getControl(99955).setVisible(False)
			if self.getControl(88455).getPosition()==[0, 0]:
				time.sleep(0.35)
				self.getControl(88455).setVisible(False)
			
		if self.getFocusId(88451) and self.getControl(88451).getLabel()=="..." :
			self.getControl(88846).setLabel( " - "+"  "+self.getControl(88850).getSelectedItem().getLabel())
			self.getControl(99955).setVisible(True)
			
		if self.getFocusId(88850) and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()== " - "+"  "+"$":
			self.getControl(88846).setLabel( " - "+"  "+self.getControl(88850).getSelectedItem().getLabel())
			self.getControl(88455).setVisible(False)
			
		if self.getFocusId(88650) and self.getControl(88451).getLabel()=="..." :
			self.getControl(88847).setLabel( " - "+"  "+self.getControl(88650).getSelectedItem().getLabel())
		
		if buttonCode == 61569 and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()== " - "+"  "+"TEST":
			
			self.getControl(88847).setLabel( " - "+"  "+"$")
			self.getControl(99955).setVisible(False)
			#time.sleep(0.35)
			self.getControl(88455).setVisible(False)
			self.getControl(88847).setVisible(False)
			
		if buttonCode == 61568 and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()== " - "+"  "+"TEST":
			
			self.getControl(88847).setLabel( " - "+"  "+"$")
			self.getControl(99955).setVisible(False)
			time.sleep(0.35)
			self.getControl(88455).setVisible(False)
			self.getControl(88847).setVisible(False)
		
		
		if buttonCode == 61568 and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()== " - "+"  "+"Tested":
			
			self.getControl(99955).setVisible(False)
			time.sleep(0.35)
			self.getControl(88455).setVisible(False)
		
		if buttonCode == 61569 and self.getControl(88451).getLabel()=="Action" and self.getControl(88847).getLabel()== " - "+"  "+"Tested":
			
			self.getControl(99955).setVisible(False)
			time.sleep(0.35)
			self.getControl(88455).setVisible(False)
		
		if self.getControl(88451).getLabel()=="...":
			
			if self.getFocusId(88650):
				self.getControl(88650).setVisible(True)
				self.getControl(88655).setVisible(True)
				self.getControl(99855).setVisible(True)
				self.getControl(88847).setLabel( " - "+"  "+self.getControl(88650).getSelectedItem().getLabel())
				self.getControl(88847).setVisible(True)
		
	
	#if ( buttonCode == 61541 and int(xbmc.getInfoLabel("Container.Position"))==0):
		#self.getControl(88850).reset()
		#self.getControl(88650).reset()
		#self.getControl(88846).setLabel("")
		#self.getControl(88845).setLabel("")
		#self.getControl(99755).setVisible(False)
		#self.getControl(88655).setVisible(False)
		#self.getControl(88650).setVisible(False)
	
	if (buttonCode==61571 ):
	
		self.getControl(88847).setLabel( " - "+"  "+"$")
		self.getControl(88847).setVisible(False)
		if self.getFocusId(88451):
			self.getControl(88650).selectItem(0)
			self.getFocusId(88650)
			if self.getControl(88451).getLabel()== "...":
				self.getControl(88847).setVisible(True)
				self.getControl(88847).setLabel( " - "+"  "+self.getControl(88650).getSelectedItem().getLabel())
			if self.getControl(88451).getLabel()== "Action" and self.getControl(88847).getLabel()!= " - "+"  "+"$" and self.getControl(88847).getLabel()!= " - "+"  "+"$$":
				self.getControl(88847).setVisible(False)
				self.getControl(88847).setLabel( " - "+"  "+"Tested")
		
		
	
	if (buttonCode==61570 and self.getControl(88847).getLabel()== " - "+"  "+"$"):		
		self.getControl(88847).setLabel( " - "+"  "+"$$")	
		self.getControl(88847).setVisible(False)
		
	if (buttonCode==61570 and self.getControl(88847).getLabel()!= " - "+"  "+"$$"):
		
		
		if self.getFocusId(88650):
			self.getFocusId(88451)
			self.getControl(88451).setLabel("Action")
			self.getControl(99855).setVisible(False)
			time.sleep(0.45)
			self.getControl(88650).setVisible(False)
			self.getControl(88655).setVisible(False)
			self.getControl(88847).setLabel("")
			self.getControl(88847).setLabel( " - "+"  "+"$")
			self.getControl(88847).setVisible(False)
	
	
	if (buttonCode==61570 and self.getControl(88847).getLabel()== ""):
			self.getFocusId(88255)

  def message(self, message):
    dialog = xbmcgui.Dialog()
    dialog.ok(" Media Insered", message)


		
mydisplay = HomidomW()
mydisplay.doModal()
del mydisplay