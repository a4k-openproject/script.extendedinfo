import xbmc
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

	def onPlayBackStarted(self):
		self.stopped = False

	def wait_for_video_end(self):
		xbmc.sleep(500)
		while not self.stopped:
			xbmc.sleep(200)
		self.stopped = False

	def wait_for_video_start(self):
		xbmc.sleep(500)
		while not xbmc.Player().isPlayingVideo():
			xbmc.sleep(200)

	def play(self, url, listitem, window=False):
		if window and window.window_type == 'dialog':
			wm.add_to_stack(window)
			window.close()
		super(VideoPlayer, self).play(item=url, listitem=listitem, windowed=False, startpos=-1)
		if window and window.window_type == 'dialog':
			self.wait_for_video_end()
			return wm.pop_stack()

	def play_from_button(self, url, listitem, window=False, dbid=0):
		if xbmc.Player().isPlayingVideo():
			xbmc.Player().stop()
		if dbid != 0 :
			item = '{"movieid": %s}' % dbid
		else:
			item = '{"file": "%s"}' % url
		Utils.get_kodi_json(method='Player.Open', params='{"item": %s, "options": {"resume": true}}' % item)
		self.wait_for_video_start()
		window.close()
		

	def OpenInfoplay(self, url, listitem, window=False, dbid=0):
		if window and window.window_type == 'dialog':
			wm.add_to_stack(window)
			window.close()
		if dbid != 0:
			item = '{"movieid": %s}' % dbid
		else:
			item = '{"file": "%s"}' % url
		Utils.get_kodi_json(method='Player.Open', params='{"item": %s, "options": {"resume": true}}' % item)
		if window and window.window_type == 'dialog':
			self.wait_for_video_end()
			return wm.pop_stack()

	def playtube(self, youtube_id=False, listitem=None, window=False):
		url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtube_id
		self.OpenInfoplay(url=url, listitem=listitem, window=window)

PLAYER = VideoPlayer()