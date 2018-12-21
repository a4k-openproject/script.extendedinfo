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

	def play(self, url, listitem, window=False):
		if window and window.window_type == 'dialog':
			wm.add_to_stack(window)
			window.close()
		super(VideoPlayer, self).play(item=url, listitem=listitem, windowed=False, startpos=-1)
		if window and window.window_type == 'dialog':
			self.wait_for_video_end()
			return wm.pop_stack()

	def OpenInfoplay(self, url, listitem, window=False, dbid=0):
		if window and window.window_type == 'dialog':
			wm.add_to_stack(window)
			window.close()
		if dbid != 0 :
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

	def play_youtube_video(self, youtube_id='', listitem=None, window=False):
		url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtube_id
		self.OpenInfoplay(url=url, listitem=listitem, window=window)

	def wait_for_video_end(self):
		xbmc.sleep(500)
		while not self.stopped:
			xbmc.sleep(200)
		self.stopped = False

PLAYER = VideoPlayer()