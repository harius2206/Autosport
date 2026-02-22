import json
import os
from entities import Track, Car, Driver

class SimpleDataContext:
    def __init__(self, filename="autosport_db.json"):
        self.filename = filename
        self.tracks = []
        self.cars = []
        self.drivers = []
        self.load()

    def create_testing_data(self):
        self.tracks = [Track("Monaco GP", 3.33, "Monaco", 1)]
        self.cars = [Car("Ferrari", "SF-24", 1000, 1)]
        self.drivers = [Driver("Charles Leclerc", 26, 1, 1)]

    def save(self):
        data = {
            "tracks": [t.__dict__ for t in self.tracks],
            "cars": [c.__dict__ for c in self.cars],
            "drivers": [d.__dict__ for d in self.drivers]
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n[Контекст] Дані успішно закешовано у {self.filename}")

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tracks = [Track(**t) for t in data.get("tracks", [])]
                    self.cars = [Car(**c) for c in data.get("cars", [])]
                    self.drivers = [Driver(**d) for d in data.get("drivers", [])]
            except:
                pass

    def is_empty(self):
        return not (self.tracks or self.cars or self.drivers)