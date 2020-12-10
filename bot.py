# import asyncio
import json
import re
import sys
from leveldata import *

class Bot:
    def __init__(self, savepath):
        self.savepath = savepath
        self.funcDict = {
            '.coins': self.fCoins,
            '.map': self.fMap,
            '.hello': self.fHello,
        }
        commRegexString = '('
        for key in self.funcDict:
            commRegexString += '(\\{})|'.format(key)
        self.commRegex = re.compile(commRegexString[:-1] + ')\\b')
        self.coins = 0
        self.run = True
        self.room = Room(width=19)
        self.player = Player()
        self.room.insert(self.player)

    def load():
        try:
            with open(self.savepath, 'r') as file:
                self.palyers = json.load(file)
        except KeyError:
            pass

    def save():
        with open(self.savepath, 'w') as file:
            json.dump(self.palyers, file)

    def loop(self, message, enter):
        if enter:
            command = self.commRegex.search(message)
            if command != None:
                self.funcDict[command.group(0)](message)

    def fCoins(self, message):
        string = 'You have {} coins\n'.format(self.coins)
        sys.stdout.write(string)

    def fMap(self, message):
        string = self.room.draw()
        sys.stdout.write(string)

    def fHello(self, message):
        sys.stdout.write(drawText("It's dengerous to go alone!\nTake this.", center=True))

class Level:
    __init__(self):
        self.rooms = []

    def addRoom(self, room):
        self.rooms.append(room)
