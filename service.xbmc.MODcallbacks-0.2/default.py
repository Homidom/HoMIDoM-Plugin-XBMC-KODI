#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012 Team-XBMC
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#    This script is based on script.randomitems & script.wacthlist
#    Thanks to their original authors

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import subprocess

__addonH__ = xbmcaddon.Addon(id='script.homixbmc')
__cwdH__         = __addonH__.getAddonInfo('path')
__iconH__        = __addonH__.getAddonInfo('icon')

pathcwdH = __cwdH__
pathiconH = __iconH__
cwdH_path = xbmc.translatePath( pathcwdH )
iconH_path = xbmc.translatePath( pathiconH )

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = __addon__.getAddonInfo('name')

script_xbmc_starts = ''
script_playerV_starts = ''
script_playerV_stops = ''
script_playerA_starts = ''
script_playerA_stops = ''
script_playerA_pauses = ''
script_playerV_pauses = ''
script_playerA_resumes = ''
script_playerV_resumes = ''
script_screensaver_starts = ''
script_screensaver_stops = ''

typevar=''


def log(txt):
    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)

class Main:
  def __init__(self):
    self._init_vars()
    self._init_property()
    global script_xbmc_starts
    if script_xbmc_starts:
      log('Going to execute script = "' + script_xbmc_starts + '"')
      xbmc.executebuiltin('XBMC.RunScript('+script_xbmc_starts+')')
    self._daemon()

  def _init_vars(self):
    self.Player = MyPlayer()
    self.Monitor = MyMonitor(update_settings = self._init_property, player_status = self._player_status)

  def _init_property(self):
	log('Reading properties')
	global script_xbmc_starts
	global script_playerV_starts
	global script_playerV_stops
	global script_playerA_starts
	global script_playerA_stops
	global script_playerV_pauses
	global script_playerA_pauses
	global script_playerA_resumes
	global script_playerV_resumes
	global script_screensaver_starts
	global script_screensaver_stops
	script_xbmc_starts = xbmc.translatePath(os.path.join((cwdH_path),"Xstart.py"))
	print "atttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
	print script_xbmc_starts
	script_playerV_starts = xbmc.translatePath(os.path.join((cwdH_path),"PVstart.py"))
	script_playerV_stops = xbmc.translatePath(os.path.join((cwdH_path),"PVStop.py"))
	script_playerA_starts = xbmc.translatePath(os.path.join((cwdH_path),"PAstart.py"))
	script_playerA_stops = xbmc.translatePath(os.path.join((cwdH_path),"PAStop.py"))
	script_playerV_pauses = xbmc.translatePath(os.path.join((cwdH_path),"PVPauses.py"))
	script_playerA_pauses = xbmc.translatePath(os.path.join((cwdH_path),"PAPauses.py"))
	script_playerA_resumes = xbmc.translatePath(os.path.join((cwdH_path),"PAResume.py"))
	script_playerV_resumes = xbmc.translatePath(os.path.join((cwdH_path),"PVResume.py"))
	script_screensaver_starts = xbmc.translatePath(os.path.join((cwdH_path),"XScreenSON.py"))
	script_screensaver_stops = xbmc.translatePath(os.path.join((cwdH_path),"XScreenSOFF.py"))
	log('script xbmc starts = "' + script_xbmc_starts + '"')
	log('script player starts = "' + script_playerV_starts + '"')
	log('script player stops = "' + script_playerV_stops + '"')
	log('script player starts = "' + script_playerA_starts + '"')
	log('script player stops = "' + script_playerA_stops + '"')
	log('script player pauses = "' + script_playerV_pauses + '"')
	log('script player pauses = "' + script_playerA_pauses + '"')
	log('script player resumes = "' + script_playerV_resumes + '"')
	log('script player resumes = "' + script_playerA_resumes + '"')
	log('script screensaver starts = "' + script_screensaver_starts + '"')
	log('script screensaver stops = "' + script_screensaver_stops + '"')
	
  def _player_status(self):
    return self.Player.playing_status()

  def _daemon(self):
    while (not xbmc.abortRequested):
      # Do nothing
      xbmc.sleep(600)
    log('abort requested')


class MyMonitor(xbmc.Monitor):
  def __init__(self, *args, **kwargs):
    xbmc.Monitor.__init__(self)
    self.get_player_status = kwargs['player_status']
    self.update_settings = kwargs['update_settings']

  def onSettingsChanged(self):
    self.update_settings()

  def onScreensaverActivated(self):
	global script_screensaver_startsx
	xbmc.executebuiltin('XBMC.RunScript('+script_screensaver_starts+ ", " + self.playing_type() +')')

  def onScreensaverDeactivated(self):
	global script_screensaver_stops
	xbmc.executebuiltin('XBMC.RunScript('+script_screensaver_stops+ ", " + self.playing_type() +')')

class MyPlayer(xbmc.Player):
  def __init__(self):
    xbmc.Player.__init__(self)
    self.substrings = [ '-trailer', 'http://' ]

  def playing_status(self):
    if self.isPlaying():
      return 'status=playing' + ';' + self.playing_type()
    else:
      return 'status=stopped'

  def playing_type(self):
    type = 'unkown'
    if type == 'unkown':
		
		oncenb=0
	  
    if (self.isPlayingAudio()):
		type = "music"
		oncenb=1
	
    if xbmc.getCondVisibility('VideoPlayer.Content(movies)'):
        filename = ''
        isMovie = True
        try:
          filename = self.getPlayingFile()
        except:
          pass
        if filename != '':
          for string in self.substrings:
            if string in filename:
              isMovie = False
              break
        if isMovie:
          type = "movie"
    if xbmc.getCondVisibility('VideoPlayer.Content(episodes)'):
        # Check for tv show title and season to make sure it's really an episode
        if xbmc.getInfoLabel('VideoPlayer.Season') != "" and xbmc.getInfoLabel('VideoPlayer.TVShowTitle') != "":
           type = "episode"
		
	#else:
		#type = 'unkown'
		
    return 'type=' + type 
  
	
  def onPlayBackStarted(self):
	log('player starts')
	global script_playerV_starts
	global script_playerA_starts
		
	if self.playing_type()!="type=music":
		LF = cwdH_path+"\\temphomixbmc2.txt"
		writefile = open(LF, 'w')
		writefile.write("video")
		writefile.close()
		log('Going to execute script = "' + script_playerV_starts + '"')
		xbmc.executebuiltin('XBMC.RunScript('+script_playerV_starts+ ", " + self.playing_type() +')')
		
	if self.playing_type()=="type=music":
		LF = cwdH_path+"\\temphomixbmc2.txt"
		writefile = open(LF, 'w')
		writefile.write("music")
		writefile.close()
		  
		log('Going to execute script = "' + script_playerA_starts + '"')
		xbmc.executebuiltin('XBMC.RunScript('+script_playerA_starts+ ", " + self.playing_type() +')')
		
		
  def onPlayBackEnded(self):
    self.onPlayBackStopped()

  def onPlayBackStopped(self):
	log('player stops')
	type = 'unkown'
	if (self.isPlayingAudio()):
	  type = "music"
	else:
		if xbmc.getCondVisibility('VideoPlayer.Content(movies)'):
			filename = ''
			isMovie = True
		try:
			filename = self.getPlayingFile()
		except:
			pass
		if filename != '':
			for string in self.substrings:
				if string in filename:
					isMovie = False
					break
		if isMovie:
			type = "movie"
		elif xbmc.getCondVisibility('VideoPlayer.Content(episodes)'):
	  # Check for tv show title and season to make sure it's really an episode
			if xbmc.getInfoLabel('VideoPlayer.Season') != "" and xbmc.getInfoLabel('VideoPlayer.TVShowTitle') != "":
				type = "episode"
	typevar=type
	
	if typevar!="music":
		global script_playerV_stops
		log('Going to execute script = "' + script_playerV_stops + '"')
		xbmc.executebuiltin('XBMC.RunScript('+script_playerV_stops+ ", " + self.playing_type()+')')
	if typevar=="music":
		global script_playerA_stops
		log('Going to execute script = "' + script_playerA_stops + '"')
		xbmc.executebuiltin('XBMC.RunScript('+script_playerA_stops+ ", " + self.playing_type()+')')
		
  def onPlayBackPaused(self):
	log('player pauses')
	global script_playerV_pauses
	global script_playerA_pauses
	
	LF = cwdH_path+"\\temphomixbmc2.txt"
	readfile = open(LF, 'r')
	for line in readfile:
		  	
		
			
			print line [0]
			if line[0]=="v":
				log('Going to execute script = "' + script_playerV_pauses + '"')
				xbmc.executebuiltin('XBMC.RunScript('+script_playerV_pauses+ ", " + self.playing_type() +')')
			
			if line[0]=="m":
				log('Going to execute script = "' + script_playerA_pauses + '"')
				xbmc.executebuiltin('XBMC.RunScript('+script_playerA_pauses+ ", " + self.playing_type() +')')
	
	
		
	
	
		  
		

  def onPlayBackResumed(self):
	global script_playerV_resumes
	global script_playerA_resumes
	
	
	LF = cwdH_path+"\\temphomixbmc2.txt"
	readfile = open(LF, 'r')
	for line in readfile:
		  	
		
			
			print line [0]
			if line[0]=="v":
				print "videoR"
				log('Going to execute script = "' + script_playerV_resumes + '"')
				xbmc.executebuiltin('XBMC.RunScript('+cwdH_path+"\PVResume.py"+ ", " + self.playing_type() +')')
			
			if line[0]=="m":
				print "musicR"
				log('Going to execute script = "' + script_playerA_resumes + '"')
				xbmc.executebuiltin('XBMC.RunScript('+cwdH_path+"\PAResume.py"+ ", " + self.playing_type() +')')


if (__name__ == "__main__"):
    log('script version %s started' % __addonversion__)
    Main()
    del MyPlayer
    del MyMonitor
    del Main
    log('script version %s stopped' % __addonversion__)
