#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime

#AWS環境変数
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REGION = os.environ['REGION']
#CAM_NO = os.environ['CAM_NO']
S3BUCKET = os.environ['S3BUCKET']
PREFIX_IN = os.environ['PREFIX_IN']
#センサー
SENSOR_NO = int(os.environ['SENSOR_NO']) #センサーNO/NC
MOTION_PIN = 21 #センサーGPIOポート

#解像度
#####################################
# 0: 176×144
# 1: 320×240
# 2: 640×480
# 3: 800×600
# 4: 1280×960
#####################################
res = 2 #デフォルト解像度設定2
resos = ([176, 144, 135, 30, 0.7],
         [320, 240, 230, 30, 1.3], 
         [640, 480, 470, 30, 2], 
         [800, 600, 585, 20, 2.2], 
         [1280, 720, 680, 5, 3.5])#解像度/録画レート/キャプション位置

#image差分動体検知をtriggerにする場合の閾値
thd = 30 #256階調grayスケールでbit判定する閾値
ratio = 0.1 #動体検知判定のための閾値(解像度に対してbit判定閾値越えした面積比率)

#映像tmpファイル録画インターバル
interval = datetime.timedelta(seconds=4) #直前の録画ループ中にセンサーが検知してなかったら4秒録画する
end_interval = datetime.timedelta(seconds=14, microseconds=150000) #直前の録画ループ中にセンサーが検知してたら14秒録画する