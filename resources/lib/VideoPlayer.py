import xbmc, xbmcgui
from resources.lib import Utils
from resources.lib.WindowManager import wm

class VideoPlayer(xbmc.Player):

	def __init__(self, *args, **kwargs):
		super(VideoPlayer, self).__init__()
		self.stopped = False

	def onPlayBackEnded(self):
		self.stopped = True

	def onPlayBackStopped(self):
		self.stopped = True

	def onLostDisplay(self):
		self.stopped = False

	def onResetDisplay(self):
		self.stopped = False

	def onPlayBackStarted(self):
		self.stopped = False

	def onAVStarted(self):
		self.stopped = False

	def wait_for_video_end(self):
		xbmc.sleep(1000)
		while not self.stopped:
			xbmc.sleep(1000)
		self.stopped = False

	def play(self, url, listitem, window=False):
		super(VideoPlayer, self).play(item=url, listitem=listitem, windowed=False, startpos=-1)
		for i in range(30):
			if xbmc.getCondVisibility('VideoPlayer.IsFullscreen'):
				if window and window.window_type == 'dialog':
					wm.add_to_stack(window)
					window.close()
					self.wait_for_video_end()
					return wm.pop_stack()
			xbmc.sleep(1000)

	def play_from_button(self, url, listitem, window=False, type='', dbid=0):
		Utils.show_busy()
		if dbid != 0:
			item = '{"%s": %s}' % (type, dbid)
			Utils.get_kodi_json(method='Player.Open', params='{"item": %s}' % item)
		else:
			item = '{"file": "%s"}' % url
			xbmc.executebuiltin('RunPlugin(%s)' % url)
		for i in range(90):
			xbmc.log(str(xbmcgui.getCurrentWindowDialogId())+'===>OPENINFO', level=xbmc.LOGNOTICE)
			if xbmcgui.getCurrentWindowDialogId() > 11999 and xbmcgui.getCurrentWindowDialogId() < 12999:
				Utils.hide_busy()
			if xbmc.getCondVisibility('VideoPlayer.IsFullscreen'):
				if window and window.window_type == 'dialog':
					wm.add_to_stack(window)
					window.close()
					self.wait_for_video_end()
					return wm.pop_stack()
			xbmc.sleep(1000)

	def playtube(self, youtube_id=False, listitem=None, window=False):
		url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtube_id
		self.play(url=url, listitem=listitem, window=window)

PLAYER = VideoPlayer()