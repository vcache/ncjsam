import copy

from dataclasses import dataclass
from typing import List

from ncjsam.etc.strings import name_to_id


class UnJson():
    def __init__(self, data):
        self._data = copy.deepcopy(data)

    def replace(self, key, func, cond=None, key_rewrite=None):
        if key in self._data:
            value = self._data[key]
            if not cond or cond(value):
                if key_rewrite:
                    self._data[key_rewrite] = func(value)
                    del self._data[key]
                else:
                    self._data[key] = func(value)
        return self

    def inject(self, key, value):
        assert key not in self._data
        self._data[key] = value
        return self

    def remove(self, key):
        self._data.pop(key)
        return self

    def done(self, Target):
        args = {
            k.replace('-', '_'): v
            for k, v in self._data.items()
        }
        return Target(**args)


@dataclass
class Path:
    parts: List[id]

    def __getitem__(self, i):
        return self.parts[i]

    def __len__(self):
        return len(self.parts)

    def mangle(self):
        return name_to_id('_'.join(self.parts))

    def as_string(self):
        return '/' + '/'.join(self.parts)

    def append(self, part):
        self.parts.append(part)

    @staticmethod
    def parse(data):
        assert data
        return Path(
            parts=data.strip('/').split('/'),
        )

    def clone(self):
        return copy.deepcopy(self)
