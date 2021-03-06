#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import cv2
import subprocess
import boto3
import parameters as para


class Emr_gen:

    def __init__(self):
        self.ACCESS_KEY = para.ACCESS_KEY
        self.SECRET_KEY = para.SECRET_KEY
        self.REGION = para.REGION
        self.s3_bucket_name = para.S3BUCKET
        self.s3_prefix = para.PREFIX_IN1 #change prefix_No if cam is cam1:PREFIX_IN1, elif is cam2:PREFIX_IN2, elif is cam3:PREFIX_IN3, elif is cam4:PREFIX_IN4
        self.emergency_dirpath = './emr/'
        self.filepath_timesorted = []
        

    #元ファイル(1.avi〜5.avi)をタイムスタンプ順に結合する関数
    def combine_file(self, emr_filename, width, heigth, fps): 

        for i in range(1,6):  #1.avi〜5.aviのタイムスタンプを取得してリストに格納
            filepath = "./tmp/0"+str(i)+".mp4" #読みだすfile名
            
            try:
                mddt = time.ctime(os.path.getmtime(filepath)) #fileのタイムスタンプを取得
                self.filepath_timesorted.append([mddt,filepath]) #データ格納順は[タイムスタンプ,filepath(i)]
            except FileNotFoundError:
                break

        list_length=len(self.filepath_timesorted) #存在するaviファイルの数をカウント(起動直後にトリガーが入ると5.aviまで揃わない)
        
        if list_length==1: #ファイルが1つだけしかない場合=起動後3秒以内にトリガー発生

            #emr_filename = location + datetime.datetime.now().strftime('%Y%m%d%H%M')#get datetime to string
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')#('M','J','P','G')#(*'mp4v')
            emr_writer = cv2.VideoWriter(self.emergency_dirpath + emr_filename +'.mp4', fourcc, fps, (width, heigth))
            
            self.filepath_timesorted[0].pop(0) #リストのタイムスタンプ部分を削除
            file_path="".join(self.filepath_timesorted[0]) #こうしないとリストからfile名がきれいに取り出せない

            cap_emr = cv2.VideoCapture(file_path)

            if cap_emr.isOpened() == True: # 最初の1フレームを読み込む
                ret,frame = cap_emr.read()
            else:ret = False
            
            while ret: # フレームの読み込みに成功している間フレームを書き出し続ける
                emr_writer.write(frame)# 読み込んだフレームを書き込み
                ret,frame = cap_emr.read()# 次のフレームを読み込
            
            subprocess.call(["sudo","rm",file_path]) #もとのaviファイルを削除する
            
        else: #ファイルが2つ以上ある場合
            self.filepath_timesorted.sort() #avifileが2つ以上ある場合はリスト中のファイル名をタイムスタンプ昇順に並べ替える
        
            for i in range(0,list_length):self.filepath_timesorted[i].pop(0) #リストのタイムスタンプ部分を削除
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')#('M','J','P','G')#(*'mp4v')
            emr_writer = cv2.VideoWriter(self.emergency_dirpath + emr_filename +'.mp4', fourcc, fps, (width, heigth))
            
            for i in range(0,list_length): #タイムスタンプの古い映像を先頭にファイルを結合する
                file_path="".join(self.filepath_timesorted[i]) #i番目のavi元file、こうしないとリストからfile名がきれいに取り出せない
                cap_emr = cv2.VideoCapture(file_path) #i番目のavi元file
                
                if cap_emr.isOpened() == True: # 最初の1フレームを読み込む
                    ret,frame = cap_emr.read()
                else:ret = False

                while ret: # フレームの読み込みに成功している間フレームを書き出して結合を続ける
                    emr_writer.write(frame)# 読み込んだフレームを書き込み
                    ret,frame = cap_emr.read()# 次のフレームを読み込
                
                subprocess.call(["sudo","rm",file_path]) #i番目のavi元ファイルを削除する
            
        emr_writer.release()
        cap_emr.release()
        self.filepath_timesorted.clear()

        self.chenge_codec(emr_filename, fps) #mp4に変換
        self.upload_awsS3(emr_filename) #s3へアップロード
        subprocess.call(["sudo","rm",self.emergency_dirpath + emr_filename + '.mp4']) #元のaviファイルを削除する


    #mp4に変換する関数
    def chenge_codec(self, emr_filename, fps):
        subprocess.call(["ffmpeg", "-i", self.emergency_dirpath + emr_filename + '.mp4', "-r", str(fps), self.emergency_dirpath + emr_filename + '-1.mp4'])

    #s3へアップロードする関数
    def upload_awsS3(self, emr_filename):
        print(emr_filename)
        s3 = boto3.client('s3', aws_access_key_id=self.ACCESS_KEY, aws_secret_access_key= self.SECRET_KEY, region_name=self.REGION)
        s3.upload_file(self.emergency_dirpath + emr_filename+"-1.mp4", self.s3_bucket_name, emr_filename+".mp4")
        print("uploaded {0}".format(emr_filename+".mp4"))
        subprocess.call(["sudo", "rm", self.emergency_dirpath + emr_filename + '-1.mp4'])
