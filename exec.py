import bot
import time
import kb as KB
import sys

ppath = 'saves/players.json'
roguebot = bot.Bot(ppath)
kb = KB.KBHit()

print('Hit ESC to exit')
chrbuf = ''
mess = ''
enter = False
prevtime = time.process_time()

while roguebot.run:

    if kb.kbhit():
        c = kb.getch()
        if ord(c) == 27: # ESC
            break
     # print(c, end='')
        if ord(c) == 127 or ord(c) == 8:
            if len(chrbuf) > 0:
                chrbuf = chrbuf[:-1]
                sys.stdout.write('\b \b')
        elif ord(c) == 10 or ord(c) == 13:
            enter = True
            mess = chrbuf
            chrbuf = ''
            sys.stdout.write('\n')
        else:
            chrbuf += c
            # sys.stdout.write(c + str(ord(c)))
            sys.stdout.write(c)
        sys.stdout.flush()

    if time.process_time() - prevtime >= 0.5:
        prevtime = time.process_time()
        roguebot.loop(mess, enter)
        if enter:
            enter = False



kb.set_normal_term()
