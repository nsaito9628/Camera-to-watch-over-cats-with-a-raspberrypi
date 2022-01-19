#!/usr/bin/python
# -*- coding: utf-8 -*-
#import wiringpi as pi
import RPi.GPIO as GPIO
import time
import parameters as para


class Sensor:
    def __init__(self):
        self.motion_pin = para.MOTION_PIN #ワークパスセンサーシグナルport : GPIO 21
        #self.dust_PIN = para.DUST_PIN #ダストセンサー：GPIO 15
        self.sensor_no = para.SENSOR_NO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_pin, GPIO.IN)
        #GPIO.setup(self.dust_PIN, GPIO.IN)
       

    def motion_detect(self): #センサーのHI/LOを1/0で出力する
        
        #sig = pi.digitalRead(self.motion_pin)

        if self.sensor_no == 1:
            if GPIO.input(self.motion_pin) == GPIO.HIGH:
                sig = 0
            else:
                sig = 1

        return sig


    def motion_count(self, motion_count): #センサーがHI出力ならカウンターをインクリメントする
        
        motion_sig = self.motion_detect()
        
        if motion_sig == 1:
            motion_count = motion_count + 1

        return motion_count

    # ダストセンサーのHIGH or LOWの時計測

    def pulseIn(self, start=1, end=0):
        if start==0: end = 1
        t_start = 0
        t_end = 0
        # ECHO_PINがHIGHである時間を計測
        while  GPIO.input(self.dust_PIN) == end:
            #i= pi.digitalRead(PIN)
            t_start = time.time()
            #print("GPIO:",i,"start:",t_start)
            
        while  GPIO.input(self.dust_PIN) == start:
            #i=pi.digitalRead(PIN)
            t_end = time.time()
            #print("GPIO:",i,"end:",t_end)
        return t_end - t_start


    # 単位をマイクログラム/m^3に変換
    def pcs2ugm3(self, pcs):
        pi = 3.14159
        #全粒子密度
        density = 1.65 * pow (10, 12)
        #PM2.5粒子の半径
        r25 = 0.44 * pow (10, -6)
        vol25 = (4/3) * pi * pow (r25, 3)
        mass25 = density * vol25
        K = 3531.5 # per m^3
        return pcs * K * mass25


    # pm2.5計測
    def get_pm25(self):
        t0 = time.time()
        t = 0
        ts = 30 #　サンプリング時間
        while True:
            # LOW状態の時間tを求める
            dt = self.pulseIn(0)
            if dt<1: t = t + dt
            
            if ((time.time() - t0) > ts):
                # LOWの割合[0-100%]
                ratio = (100*t)/ts
                #　ホコリの濃度を算出
                concent = 1.1 * pow(ratio,3) - 3.8 * pow(ratio,2) + 520 * ratio + 0.62         
                dust_count = self.pcs2ugm3(concent)
                if dust_count < 0: dust_count = 0 
                return dust_count
