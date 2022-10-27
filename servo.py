import time
import RPi.GPIO as GPIO
import os

class VoiceSpeech():
    def __init(self):
        print("VoiceSpeech init")

    def yoshi(self):
        print("yoshi")
        os.system('mpg321 ./voice/yoshi.mp3')

    def voice_play(sentence):
        print(sentence)
        os.system('mpg321 ./voive/' + sentence + ".mp3")

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
p = GPIO.PWM(4, 50)

vs = VoiceSpeech()

def yoshi_motion():
    global p, vs
    print("yoshi!")
    vs.voice_play(yoshi)
    p.ChangeDutyCycle(7)
    time.sleep(0.4)
    p.ChangeDutyCycle(4)
    time.sleep(0.4)
    
def main():
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    p.start(0.0)
    p.ChangeDutyCycle(0.0)
    
    while True:
        a = input()
        if a == 'yoshi':
            yoshi_motion()

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
