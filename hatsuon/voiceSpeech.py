import os
import sys 

class VoiceSpeech():
    def __init__(self):
        print('VoiceSpeech Init')

    def yoshi(self):
        print(sys._getframe().f_code.co_name)
        os.system('afplay ./voice/yoshi.mp3')

    def ashimoto(self):
        print(sys._getframe().f_code.co_name)
        os.system('afplay ./voice/ashimoto.mp3')

    def koegachiisai(self):
        print(sys._getframe().f_code.co_name)
        os.system('afplay ./voice/koegachiisai.mp3')

    def goanzenni(self):
        print(sys._getframe().f_code.co_name)
        os.system('afplay ./voice/goanzenni.mp3')
