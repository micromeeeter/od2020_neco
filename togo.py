import os
import time
from datetime import datetime

import cv2

import RPi.GPIO as GPIO

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


# _________camera settings________
# /dev/video0を指定
DEV_ID = 0
# パラメータ
WIDTH = 640
HEIGHT = 480
FPS = 30
# 録画時間(秒)
REC_SEC = 10
#_________________________________

# _________ GPIO settings ________
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
p = GPIO.PWM(4, 50)
# _________________________________