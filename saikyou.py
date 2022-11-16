import time
import threading
import RPi.GPIO as GPIO
import os

class VoiceSpeech():
    def __init(self):
        print("VoiceSpeech init")

    def voice_play(self, sentence):
        print(sentence)
        command = "./jtalk.sh " + str(sentence)
        os.system(command)

PIN_SERVO = 4
PIN_SENSOR = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SERVO, GPIO.OUT)
GPIO.setup(PIN_SENSOR, GPIO.IN)

p = GPIO.PWM(PIN_SERVO, 50)

vs = VoiceSpeech()

def yoshi_motion(num=0):
    global p
    p.ChangeDutyCycle(int(num))

def yoshi_voice(comm=""):
    global vs
    vs.voice_play(comm)

def yoshi(comm):
    global p
    print("bang")
    t_motion = threading.Thread(target=yoshi_motion, args=(int(7),))
    t_voice = threading.Thread(target=yoshi_voice, args=(comm,))
    t_voice.start()
    time.sleep(1)
    t_motion.start()
    time.sleep(1)
    p.ChangeDutyCycle(4)

    t_motion = threading.Thread(target=yoshi_motion, args=(int(7),))
    t_voice = threading.Thread(target=yoshi_voice, args=("よし",))
    t_voice.start()
    time.sleep(1.3)
    t_motion.start()
    time.sleep(1)
    p.ChangeDutyCycle(4)
    time.sleep(0.3)

def main():
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    p.start(0.0)
    p.ChangeDutyCycle(0.0)

    p_sensor = False

    while True:
        sensor = False
        print(GPIO.input(PIN_SENSOR))
        if GPIO.input(PIN_SENSOR) == GPIO.HIGH:
            sensor = True
        else:
            sensor = False
        if p_sensor == False and sensor == True:
            yoshi("中盛")
            yoshi("テイクアウト")
            yoshi("割り箸")

        p_sensor = sensor

        time.sleep(1)

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
