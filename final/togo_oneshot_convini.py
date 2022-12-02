import os
import random
import time
import threading
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
PIN_SERVO = 4
PIN_SENSOR = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SERVO, GPIO.OUT)
GPIO.setup(PIN_SENSOR, GPIO.IN)

p = GPIO.PWM(PIN_SERVO, 50)# p is GPIO's PWN "P"!!
#_________________________________

#_________VoiceSpeechDefine_______
class VoiceSpeech():
    def __init(self):
        print("VoiceSpeech init")

    def voice_play(self, sentence):
        print(sentence)
        command = "./jtalk.sh " + str(sentence)
        os.system(command)

vs = VoiceSpeech()
#_________________________________


#________YOSHI IKUZOU______________
def yoshi_motion(num=0):
    global p

    p.ChangeDutyCycle(int(num))
    #num is servo angle

def yoshi_voice(comm=""):
    global vs
    vs.voice_play(comm)

def yoshi(comm):
    global p
    print("bang")
    t_motion = threading.Thread(target=yoshi_motion, args=(int(6),))
    t_voice = threading.Thread(target=yoshi_voice, args=(comm,))
    t_voice.start()
    time.sleep(1)
    t_motion.start()
    time.sleep(1)
    p.ChangeDutyCycle(4)

    t_motion = threading.Thread(target=yoshi_motion, args=(int(6),))
    t_voice = threading.Thread(target=yoshi_voice, args=("よし",))
    t_voice.start()
    time.sleep(1.3)
    t_motion.start()
    time.sleep(1)
    p.ChangeDutyCycle(4)
    time.sleep(0.3)
#_________________________________


#_________Google Authorize________
def google_auth():
    global drive
    #Googleサービスを認証
    gauth = GoogleAuth()
    #資格情報ロードするか、存在しない場合は空の資格情報を作成
    gauth.LoadCredentialsFile("mycreds.txt")
    #Googleサービスの資格情報がない場合
    if gauth.credentials is None:
        #ユーザーから認証コードを自動的に受信しローカルWebサーバーを設定
        gauth.LocalWebserverAuth()
    #アクセストークンが存在しないか、期限切れかの場合
    elif gauth.access_token_expired:
        #Googleサービスを認証をリフレッシュする
        gauth.Refresh()
    #どちらにも一致しない場合
    else:
        #Googleサービスを承認する
        gauth.Authorize()
    #資格情報をtxt形式でファイルに保存する
    gauth.SaveCredentialsFile("mycreds.txt")
    #Googleドライブの認証処理
    drive = GoogleDrive(gauth)

    print("g auth ok")
#_________________________________

#______record and upload__________
def record_and_upload():
    global drive, WIDTH, HEIGHT, FPS, REC_SEC
    cap = cv2.VideoCapture(DEV_ID)
    # パラメータの指定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    # ファイル名に日付を指定
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = "log/" +  date + ".mp4"
    # 動画パラメータの指定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(name, fourcc, FPS, (WIDTH, HEIGHT))

    # キャプチャ
    for _ in range(FPS * REC_SEC):
        ret, frame = cap.read()
        out.write(frame)

    #アップロードするフォルダパス指定
    path = r"/home/pi/Desktop/od2020_neco/log/"
    #GoogleDriveFileオブジェクト作成
    f = drive.CreateFile({'title' : name})
    #ローカルのファイルをセットしてアップロード
    f.SetContentFile(os.path.join(path,name))
    #Googleドライブにアップロード
    f.Upload()
    f = None

    # 後片付け
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return

    #_________________________________

def record_and_upload_oneshot():
    global WIDTH, HEIGHT, drive
    cap = cv2.VideoCapture(DEV_ID)

    # 解像度の指定                                                                      
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = "./log/"
    name = date + ".jpg"
    
    # キャプチャの実施                                                                  
    ret, frame = cap.read()
    if ret:
        # ファイル名に日付を指定
        cv2.imwrite(path+name, frame)

        #アップロードするフォルダパス指定                                                   
    path = r"/home/pi/Desktop/od2020_neco/log/"
    #GoogleDriveFileオブジェクト作成                                                    
    f = drive.CreateFile({'title' : path})
    #ローカルのファイルをセットしてアップロード                                         
    f.SetContentFile(os.path.join(path,name))
    #Googleドライブにアップロード                                                       
    f.Upload()
    f = None

    # 後片付け                                                                          
    cap.release()
#    out.release()
    cv2.destroyAllWindows()
    return


    # 後片付け                                                                          
    cap.release()
    cv2.destroyAllWindows()
    return


def main():
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    p.start(0.0)
    p.ChangeDutyCycle(0.0)

    google_auth()

    iukoto = [
        ["ネームプレート", "サンタ帽子", "トナカイの鼻"],
        ["消毒アルコール", "マスク" , "換気"],
        ["掃除", "金庫", "報告"]
    ]
    
    p_sensor = False

    t_motion = threading.Thread(target=yoshi_motion, args=(int(7),))
#    thread_record_and_upload = threading.Thread(target=record_and_upload, args=())
    #thread_record_and_upload(target=record_and_upload())

    counter = 0
    while True:
        sensor = False
        print(GPIO.input(PIN_SENSOR))
        if GPIO.input(PIN_SENSOR) == GPIO.HIGH:
            sensor = True
        else:
            sensor = False
        if p_sensor == False and sensor == True and counter > 20:
            thread_record_and_upload = threading.Thread(target=record_and_upload_oneshot, args=())
            thread_record_and_upload.start()
            rand = random.randrange(3)
            for i in range(3):
                yoshi(iukoto[rand][i])
            #yoshi("中盛")
            #yoshi("テイクアウト")
            #yoshi("割り箸")
            yoshi_voice("ご安全に")
            counter = 0

        p_sensor = sensor
        counter += 1
        time.sleep(1)



try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
