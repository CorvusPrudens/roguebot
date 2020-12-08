import bot
import time
import kb as KB

ppath = 'saves/players.json'
roguebot = bot.Bot(ppath)


while (roguebot.run):
	roguebot.loop()
	time.sleep(1)

 kb = KB.KBHit()

print('Hit any key, or ESC to exit')
chrbuf = ''
mess = ''
enter = False
prevtime = time.process_time()

while roguebot.run::

    if kb.kbhit():
        c = kb.getch()
        if ord(c) == 27: # ESC
            break
     # print(c, end='')
        if ord(c) == 127:
            if len(chrbuf) > 0:
                chrbuf = chrbuf[:-1]
                sys.stdout.write('\b \b')
        elif ord(c) == 10:
            enter = True
            mess = chrbuf
            chrbuf = ''
        else:
            chrbuf += c
            sys.stdout.write(c + str(ord(c)))
        sys.stdout.flush()

    if time.process_time() - prevtime >= 1:
        prevtime = time.process_time()
        roguebot.loop(mess, enter)

    

kb.set_normal_term()
