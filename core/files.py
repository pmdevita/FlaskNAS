import os
from pathlib import Path
import core.constants as consts
from core.utils import validate_path


class InvalidPath(Exception):
    pass


class Files:
    def __init__(self, config):
        self._config = config
        # self.tree = list(os.walk(self._config["rootpath"]))

    def list_shares(self):
        return self._get_files_folders(self._config["rootpath"])[0]

    def get_listing(self, path):
        if not validate_path(self._config["rootpath"], path):
            print('invalid path')
            raise InvalidPath
        path = os.path.join(self._config["rootpath"], path)
        print(os.path.isdir(path))
        if not os.path.isdir(path):
            raise InvalidPath
        children = self._get_files_folders(path)
        return self._get_size_dates(path, children)

    def _get_files_folders(self, path):
        dirs = []
        files = []
        for i in os.scandir(path):
            if i.is_dir():
                dirs.append(i.name)
            else:
                files.append(i.name)
        return (dirs, files)

    def _get_size_dates(self, path, children):
        dirs = []
        files = []
        for i in children[0]:
            dirs.append((i, os.path.getmtime(os.path.join(path, i))))
        for i in children[1]:
            files.append((i, os.path.getmtime(os.path.join(path, i)), os.path.getsize(os.path.join(path, i))))
        return [dirs, files]