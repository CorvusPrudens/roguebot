# import asyncio
import json
import re
import sys

class Bot:
    def __init__(self, savepath):
        self.savepath = savepath
        self.funcDict = {
            '.coins': self.fCoins,
            '.map': self.fMap,
        }
        commRegexString = '('
        for key in self.funcDict:
            commRegexString += '(\\{})|'.format(key)
        self.commRegex = re.compile(commRegexString[:-1] + ')\\b')
        self.coins = 0
        self.run = True

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
        pass

    def fCoins(self, message):
        string = 'You have {} coins\n'.format(self.coins)
        sys.stdout.write(string)

    def fMap(self, message):
        string = '.....\n'
        sys.stdout.write(string)
