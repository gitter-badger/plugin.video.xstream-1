import os
import xbmcaddon
from xbmc import translatePath

addonID = 'plugin.video.xstream'
addon = xbmcaddon.Addon(id = addonID)
addonPath = translatePath(addon.getAddonInfo('path')).decode('utf-8')
profilePath = translatePath(addon.getAddonInfo('profile')).decode('utf-8')

CACHE_PATH = os.path.join(profilePath, 'htmlcache')
LOCAL_STORAGE_PATH = os.path.join(profilePath, 'local_storage')