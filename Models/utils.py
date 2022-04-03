import json


class ToStrMixin:
    def __str__(self):
        return f'{self.__class__.__name__}: {json.dumps(self, default=lambda o: o.__dict__)}'
