class Track:
    def __init__(self, name, length, country, id=None):
        self.id = id
        self.name = name
        self.length = length
        self.country = country

    def __str__(self):
        return f"Траса: {self.name} | {self.country} | {self.length} км [ID: {self.id}]"

class Car:
    def __init__(self, brand, model, power, id=None):
        self.id = id
        self.brand = brand
        self.model = model
        self.power = power

    def __str__(self):
        return f"Авто: {self.brand} {self.model} | {self.power} к.с. [ID: {self.id}]"

class Driver:
    def __init__(self, name, age, car_id, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.car_id = car_id

    def __str__(self):
        return f"Гонщик: {self.name} | Вік: {self.age} | Авто ID: {self.car_id} [ID: {self.id}]"

# Файл: entities.py (доповнено моделями для представлення)

class TrackBrowsingModel:
    def __init__(self, id, name, country, length):
        self.id = id
        self.name = name
        self.country = country
        self.length = length

    @staticmethod
    def from_entity(track):
        return TrackBrowsingModel(
            id=track.id,
            name=track.name,
            country=track.country,
            length=track.length
        )

class TrackEditingModel:
    def __init__(self, id=None, name="", country="", length=0.0, note=""):
        self.id = id
        self.name = name
        self.country = country
        self.length = length
        self.note = note

    @staticmethod
    def from_entity(track):
        if not track: return None
        return TrackEditingModel(
            id=track.id,
            name=track.name,
            country=track.country,
            length=track.length,
            note=getattr(track, 'note', "")
        )

    def to_entity(self):
        from entities import Track
        return Track(
            name=self.name,
            length=self.length,
            country=self.country,
            id=self.id
        )