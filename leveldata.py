import math
import copy
import numpy as np


# IDEA -- there could be a weak light/lamp that only
# illuminates a part of the room (making going to the middle
# and using the item an interesting choice)

concept1 = '''█▀▀▀▒▒▀▀▀█
█        █
▒▒   P  ▒▒
█        █
█▄▄▄▒▒▄▄▄█
'''

concept2 = '''╔═════════════════════════╗
║ Hello weary traveler... ║
╚═════════════════════════╝
'''

textBox = {
    'ul': '╔',
    'ur': '╗',
    'ud': '═',
    'lr': '║',
    'dl': '╚',
    'dr': '╝',
}

def drawText(string, center=False):
    lines = string.split('\n')
    longestLine = 0
    numlines = 1
    for line in lines:
        if len(line) > longestLine:
            longestLine = len(line)
    for char in string:
        if char == '\n':
            numlines += 1
    output = textBox['ul'] + textBox['ud']*(longestLine + 2) + textBox['ur'] + '\n'
    # if center:
        # there's probably a way to center with formatting
        # formatter = '{} {: >?} {: >!}\n'.replace('?', str(longestLine/2))
    # else:
    formatter = '{} {: <?} {}\n'.replace('?', str(longestLine))
    print(formatter)
    for line in lines:
        output += formatter.format(textBox['lr'], line, textBox['lr'])
    return output + textBox['dl'] + textBox['ud']*(longestLine + 2) + textBox['dr'] + '\n'

tiles = {
    'opaque': '█',
    'opaque_up': '▀',
    'opaque_down': '▄',
    'semi-opaque': '▓',
    'semi-transparent': '▒',
    'transparent': '░',
    'void': ' ',
}

flat = {
    (0, 0): 'void',
    (0, 4): 'opaque_down',
    (4, 0): 'opaque_up',
    (4, 4): 'opaque',
    (1, 1): 'semi-opaque',
    (1, 4): 'opaque_down',
    (4, 1): 'opaque_up', 
    (2, 2): 'semi-transparent',
    (2, 4): 'opaque_down',
    (4, 2): 'opaque_up', 
    (3, 3): 'transparent',
    (3, 4): 'opaque_down',
    (4, 3): 'opaque_up', 
}

# NOTE for map data -- 
# 0 = opaque pixel
# 1 = semi-opaque
# 2 = semi-transparent
# 3 = transparent
# 4 = void

roomTemplate = {
    'name': 'room',
    'width' : -1,
    'height': -1,
    'map': [],
}

sqRoom = {
    'name': 'square',
    'width': 5,
    'height': 5,
    'map': [
        4, 4, 4, 4, 4,
        4, 0, 0, 0, 4, 
        4, 0, 0, 0, 4,
        4, 0, 0, 0, 4,
        4, 4, 4, 4, 4,
    ]
}

def od(x, y, width):
    return int(x + y*width)

def formatRoom(roomdict):
    w = roomdict['width'] + 4
    h = roomdict['height']*2 + 4
    # for final discord use:
    # output = '```'
    output = ''
    mapp = roomdict['map']
    # print(math.ceil(h/2))
    for y in range(math.ceil(h/2)):
        for x in range(w):
            pos1 = od(x, y*2, w)
            pos2 = od(x, y*2 + 1, w)
            # print(pos1, pos2)
            try:
                output += tiles[flat[(mapp[pos1], mapp[pos2])]]
            except IndexError:
                # print(flat[(mapp[pos1]), mapp[pos1]])
                output += tiles[flat[(mapp[pos1], 0)]]
            except KeyError:
                print('Error: room {} is poorly formatted!'.format(roomdict['name']))
                exit(1)
        output += '\n'
    # for final discord use:
    # output += '```'
    return output

def genRoom(name, width, height, shape, fill=False):
    dict = copy.deepcopy(roomTemplate)
    dict['name'] = name
    dict['width'] = width
    dict['height'] = height
    width += 4
    height = height*2 + 4
    tempmap = np.zeros((width*height,), dtype='u1')

    # note -- this will cause errors if the height is less than four
    if shape == 'rect':
        for y in range(height):
            for x in range(width):
                if y == 0:
                    tempmap[od(x, y, width)] = 4
                elif y == height - 1:
                    tempmap[od(x, y, width)] = 4
                if x == 0:
                    tempmap[od(x, y, width)] = 4
                elif x == width - 1:
                    tempmap[od(x, y, width)] = 4

                if fill:
                    if x > 1 and x < width - 2 and y > 1 and y < height - 2:
                        tempmap[od(x, y, width)] = 3

        # doors (hardcoded 2 pixels)
        if height % 2 == 0:
            tempmap[od(0, height/2 - 1, width)] = 0
            tempmap[od(0, height/2, width)] = 0
            tempmap[od(width - 1, height/2 - 1, width)] = 0
            tempmap[od(width - 1, height/2, width)] = 0
        else:
            tempmap[od(0, math.floor(height/2), width)] = 0
            tempmap[od(width - 1, math.floor(height/2), width)] = 0

        if width % 2 == 0:
            tempmap[od(width/2 - 1, 0, width)] = 0
            tempmap[od(width/2, 0, width)] = 0
            tempmap[od(width/2 - 1, height - 1, width)] = 0
            tempmap[od(width/2, height - 1, width)] = 0
        else:
            tempmap[od(width/2, 0, width)] = 0
            tempmap[od(width/2, height - 1, width)] = 0
         
    dict['map'] = tempmap
    return dict                                

bigg = genRoom('sq', 18, 9, 'rect', fill=True)

def printRoom(roomdict):
    for y in range(roomdict['height']):
        string = ''
        for x in range(roomdict['width']):
            string += str(roomdict['map'][od(x, y, roomdict['width'])])
        print(string)
         
# printRoom(bigg)

class Room:
    def __init__(self, name='chamber', width=18, height=9, shape='rect'):
        self.dict = genRoom(name, width, height, shape, fill=True)
        self.buffer = formatRoom(self.dict)
        self.things = []

    def draw(self):
        tempbuff = self.buffer
        for thing in self.things:
            tempbuff = self.add(tempbuff, thing)
        return tempbuff

    def add(self, buff, thing):
        pos = self.buff2coord(thing.dict['x'], thing.dict['y'])
        return buff[:pos] + thing.dict['char'] + buff[pos + 1:]

    def buff2coord(self, x, y):
        # + 5 instead of 4 because of newline
        return (x + 2) + (y + 1)*(self.dict['width'] + 5)

    def insert(self, thing):
        self.things.append(thing)
               
class Thing:
    def __init__(self):
        self.dict = {}

class Player(Thing):
    def __init__(self, name='Player', char='P'):
        self.dict = {
            'name': name,
            'x': 9,
            'y': 4,
            'char': char,
        }
