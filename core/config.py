import json
import core.constants as consts

class Config:
    def __init__(self):
            try:
                with open(consts.CONFIG) as f:
                    self._config = json.load(f)
            except FileNotFoundError:
                self._config = {}
            self.keys = self._config.keys

    def _save(self):
        with open(consts.CONFIG, "w") as f:
            json.dump(self._config, f)

    def __getitem__(self, item):
        return self._config.__getitem__(item)

    def __setitem__(self, key, value):
        self._config.__setitem__(key, value)
        self._save()
