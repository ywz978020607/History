import time,_thread

color_num = 10

def main1():
    global  color_num
    while 1:
        print("main1:",color_num)

def change():
    global  color_num
    color_num += 1

def main2():
    while 1:
        change()
    time.sleep(1)

_thread.start_new_thread(main2,())

main1()