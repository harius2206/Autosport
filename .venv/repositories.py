from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def get_all(self): pass
    @abstractmethod
    def add(self, item): pass
    @abstractmethod
    def get_by_id(self, id): pass
    @abstractmethod
    def delete(self, id): pass

class BaseRepository(IRepository):
    def __init__(self, collection):
        self._collection = collection

    def get_all(self):
        return self._collection

    def get_by_id(self, id):
        return next((x for x in self._collection if x.id == id), None)

    def add(self, item):
        max_id = max([x.id for x in self._collection], default=0)
        item.id = max_id + 1
        self._collection.append(item)

    def delete(self, id):
        item = self.get_by_id(id)
        if item:
            self._collection.remove(item)

class AutosportUnitOfWork:
    def __init__(self, data_context):
        self._context = data_context
        self.tracks = BaseRepository(data_context.tracks)
        self.cars = BaseRepository(data_context.cars)
        self.drivers = BaseRepository(data_context.drivers)

    def save(self):
        self._context.save()