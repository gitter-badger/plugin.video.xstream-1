import os
import pickle

from resources.lib import common, logger


class LocalStorage(object):
    _data = {}

    def __init__(self):
        super(LocalStorage, self).__init__()
        self._local_storage_file = self._get_file_name()
        self._load()

    def _get_file_name(self):
        class_name = type(self).__name__

        local_storage_path = os.path.join(common.profilePath, 'local_storage')
        if not os.path.exists(local_storage_path):
            os.makedirs(local_storage_path)

        return os.path.join(local_storage_path, class_name)

    def _load(self):
        if os.path.exists(self._local_storage_file):
            self._data = pickle.load(open(self._local_storage_file, 'rb'))

    def _save(self):
        pickle.dump(self._data, open(self._local_storage_file, 'wb'))

    def set_data(self, key, value):
        self._data[key] = value
        self._save()

    def get_data(self, key):
        if self._data and key in self._data:
            return self._data[key]
        return None

    def del_data(self, key):
        if self._data and key in self._data:
            del self._data[key]