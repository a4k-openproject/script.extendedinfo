import sys
import xbmc

def main():
	base = 'RunScript(script.extendedinfo,info='
	info = sys.listitem.getVideoInfoTag()
	dbid = info.getDbId()
	if not dbid:
		dbid  = sys.listitem.getProperty('dbid')
	remote_id = sys.listitem.getProperty('id')
	db_type   = info.getMediaType()
	if db_type   == 'movie':
		xbmc.executebuiltin('%sextendedinfo,dbid=%s,id=%s,imdb_id=%s,name=%s)' % (base, dbid, remote_id, info.getIMDBNumber(), info.getTitle()))
	elif db_type == 'tvshow':
		xbmc.executebuiltin('%sextendedtvinfo,dbid=%s,id=%s,name=%s)' % (base, dbid, remote_id, info.getTVShowTitle()))
	elif db_type == 'season':
		xbmc.executebuiltin('%sseasoninfo,dbid=%s,id=%s,tvshow=%s,season=%s)' % (base, dbid, remote_id, info.getTVShowTitle(), info.getSeason()))
	elif db_type == 'episode':
		xbmc.executebuiltin('%sextendedepisodeinfo,dbid=%s,id=%s,tvshow=%s,season=%s,episode=%s)' % (base, dbid, remote_id, info.getTVShowTitle(), info.getSeason(), info.getEpisode()))
	elif db_type in ['actor', 'director']:
		xbmc.executebuiltin('%sextendedactorinfo,name=%s)' % (base, sys.listitem.getLabel()))

if __name__ == '__main__':
	main()