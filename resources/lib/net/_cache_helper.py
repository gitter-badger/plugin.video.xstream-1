import hashlib
import os
import pickle
import time

from resources.lib import common, logger
from resources.lib.config import cConfig


class CacheHelper(object):
    def __init__(self, url=None):
        self._set_cache_path()

        if url:
            self._set_cache_file_name(url)

    def _set_cache_path(self, cache_path=None):
        self._cache_path = None
        if not cache_path:
            cache_path = common.CACHE_PATH
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        self._cache_path = cache_path

    def _set_cache_file_name(self, url):
        self._cache_file_name = None
        url_hash = hashlib.md5(url).hexdigest()
        self._cache_file_name = os.path.join(self._cache_path, url_hash)

    def _get_file_age(self, cache_file):
        try:
            file_age = time.time() - os.stat(cache_file).st_mtime
        except:
            return None
        return file_age

    def load_chache(self):
        try:
            return pickle.load(open(self._cache_file_name, 'rb'))
        except IOError as e:
            logger.info('No cache available')
            return None

    def save_cache(self, response):
        pickle.dump(response, open(self._cache_file_name, 'wb'))

    @classmethod
    def has_cache(cls, url):
        ch = cls(url)
        return os.path.exists(ch._cache_file_name)

    @classmethod
    def clean_cache(cls, expire_time=None):
        ch = cls()

        if not expire_time:
            expire_time = int(cConfig().getSetting('cacheTime'))

        files = os.listdir(ch._cache_path)
        for file in files:
            cache_file = os.path.join(ch._cache_path, file)
            file_age = ch._get_file_age(cache_file)
            if not file_age or file_age > expire_time:
                os.remove(cache_file)