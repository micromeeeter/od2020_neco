import cv2
from datetime import datetime

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

# /dev/video0を指定
DEV_ID = 0
# パラメータ
WIDTH = 640
HEIGHT = 480
FPS = 30
# 録画時間(秒)
REC_SEC = 10

def main():
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

    # /dev/video0を指定
    cap = cv2.VideoCapture(DEV_ID)
    # パラメータの指定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    # ファイル名に日付を指定
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = date + ".mp4"
    # 動画パラメータの指定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(name, fourcc, FPS, (WIDTH, HEIGHT))

    # キャプチャ
    for _ in range(FPS * REC_SEC):
        ret, frame = cap.read()
        out.write(frame)

    #アップロードするフォルダパス指定
    path = r"/home/pi"
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


if __name__ == "__main__":
    main()
