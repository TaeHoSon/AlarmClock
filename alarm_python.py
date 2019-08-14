import bluetooth
from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from time import sleep, strftime
import time
import getCurrentTime
import threading

lcd = Adafruit_CharLCD()
lcd.begin(16,1)
buzzer = Buzzer(17)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
uuid ="94f39d29-7d6d-497d-973b-fba39e49d4ee"
bluetooth.advertise_service(server_socket, "samepleServer",
                            service_id = uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles = [bluetooth.SERIAL_PORT_PROFILE], )


realTime_Hour = ""
realTime_Minute =""
str_hour=""
str_minute =""
alarmFlag = 1

getCurrentTime.TaskCurrentTime()


def alarm_On() :
    print('Alarm on')
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)

def alarm_Off():
    print ('Alarm off')
    buzzer.off()
    rdata = "Alarm Off"
    client_socket.send(rdata + '\r\n')


def show_s():
    a = int(data)
    b = time.ctime(a/1000)
    c = time.strftime('%b %d  %H:%M:%S', time.localtime(a/1000))
    d = datetime.strptime(c, '%b %d  %H:%M:%S')
    return d

def set_time():
    a = int(data)
    b = time.ctime(a/1000)
    c = time.strftime('%b %d  %H:%M:%S', time.localtime(a/1000))
    return c

def CheckTime():
    global alarmFlag
    realTime_Hour = getCurrentTime.hour
    realTime_Minute = getCurrentTime.minute
    str_hour = show_s().hour
    str_minute = show_s().minute
    if (realTime_Hour == str_hour and realTime_Minute == str_minute and alarmFlag ==1):
        timer.cancel()
        alarm_On()
        alarmFlag = 0
    if ( alarmFlag ==0 and input_state==False ):
        alarm_Off()

client_socket,address = server_socket.accept()
print ("accepted :" , address)

try:
    data = client_socket.recv(1024)
    data = data.decode('utf-8').strip()
    print ('received : ' + data )
    print ('Alarm set : ' + set_time() )
    timer = threading.Timer(1,CheckTime)
    timer.start()
    while 1:      
        input_state = GPIO.input(18)
        CheckTime()
        lcd.clear()
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        lcd.message(datetime.strftime(show_s(), 'Alarm set %H:%M'))
        time.sleep(1)
        
except KeyboardInterrupt:
    print('CTRL-C pressed.  Program exiting...')
    exit
    
client_socket.close()
server_socket.close()
