# import asyncio
import json

class Bot:
    def __init__(self, savepath):
    self.savepath = savepath
        pass

    def load():
        try: 
            with open(self.savepath, 'r') as file:
                self.palyers = json.load(file)
        except KeyError:
            pass

    def save():
        with open(self.savepath, 'w') as file:
            json.dump(self.palyers, file)

    def loop(self):
        pass
