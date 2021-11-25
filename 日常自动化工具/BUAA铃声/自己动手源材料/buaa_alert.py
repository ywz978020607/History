from playsound import playsound
import datetime
import time

open_time = ['08:00','08:50','09:50','10:40','14:00','14:50','15:50','16:40']
close_time = ['08:45','09:35','10:35','11:25','14:45','15:45','16:35','17:25']
last_time = '00:00'

while 1:
    try:
        temp_time = datetime.datetime.now().strftime('%H:%M')
        if temp_time is not last_time:
            last_time = temp_time
            if temp_time in open_time:
                playsound('1.mp3')
            if temp_time in close_time:
                playsound('2.mp3')
    except:
        print("error")
        pass

    time.sleep(30) #30s

# playsound('1.mp3')

# playsound('2.mp3')






