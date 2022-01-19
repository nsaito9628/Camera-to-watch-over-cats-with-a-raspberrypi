# Camera-to-watch-over-cats-with-a-raspberrypi
It is a self-made system that watches the daily life of remote families and cats with Raspberry Pi, cheap sensor, USB camera and AWS.  (日本語名：ニャンコ見守りカメラ)
<br>
## **What can be done**
The movement and dustiness (pm2.5 count) of people and pets in the installed room are displayed on the web screen at 10-minute intervals.  

Data is not saved in DB 
<br>
<br>

## **Architecture**
<br />
<img src="img/architecture.PNG">
<br />
<br />

## **Event recording work flow**
<br />
<img src="img/event_recorder_work_flow.PNG">
<br />
<br />

## **Web screen view sample**
<br />
<img src="img/web screen view.PNG">
<br />
<br />
<br />

## **Physical specifications**
### **Sensor**

For detection of objects such as people：  
* E18-D80NK  (datasheet: ./pdf/e18-d80nk.pdf)  
* HC-SR501  (datasheet: ./pdf/HC-SR501.pdf)  
<br>

#### **RaspberryPi**
Hardware: armv7l  
Model: Raspberry Pi 3 Model B Plus Rev 1.3  
microSD card: 32GB or more
<br>
<br />

## **Development environment**
#### **RaspberryPi**
Kernel: Linux    
Kernel release No.: 5.4.72-v7+  
Kernel version: #1356 SMP Thu Oct 22 13:56:54 BST 2020  
OS： Raspbian GNU/Linux 10 (buster)  
Language: python 3.7.3
#### **Windows**
Editor: VSCode  
VSCode expantions: Python、Pylance、MagicPython、GitLens、Git Histry、Git Graph、Markdown All in One、Excel to Markdown table  
SCP client: WinSCP ver. 5.19  
SSH terminal client: TeraTerm ver. 4.105  
<br>
<br>

## **Construction procedure**
### **Preparation**
1.  Prepare RaspberryPi OS image disc.  https://www.raspberrypi.com/software/
2.  Register Raspberry Pi to NW connected to the Internet.
3.  Prepare an aws account.
4.  Prepare IAM user with 8 policies of ./user_policy and AWSIoTFullAccess attached, or IAM user with administrator authority attached so that both console login and access key can be used.  You must replace "accountID" to your accountID in 8policies.
5.  Prepare IAM role named as "basic_lambdaexec" to resolve dependences among Resources, is Consists of AmazonS3FullAccess, CloudFrontFullAccess and AWSLambdaBasicExecutionRole.
6. Download access key ID and secret access key.
<br>

### **Building an environment on Raspberry Pi**
Launch Raspberry Pi that can connect to the Internet.  
  
Packages introduction
```sh
sudo apt update  
sudo apt -y upgrade  
python3 -m pip install --upgrade pip  
sudo apt install -y postfix git docker
sudo apt install libatlas-base-dev libjasper-dev
sudo apt install ffmpeg  libcanberra-gtk3-module v4l-utils qv4l2 -y
pip3 install awscli aws-sam-cli boto3 --upgrade
pip3 install opencv-python==4.5.1.48

cd /usr/bin
sudo rm python
sudo ln -s python3 python
cd
```
  
Set aws configuration as default profile  
```sh
aws configure (Replace with your own key)  
    AWS Access Key ID[]: your Access Key ID
    AWS Secret Access Key []: your Secret Access Key
    Default region name []: ap-northeast-1
    Default output format []:
```
  
Clone this project from public repository
```sh  
git clone https://github.com/nsaito9628/Camera-to-watch-over-cats-with-a-raspberrypi.git
```
  
Deploy a Python project  
``` sh
sudo cp ./Camera-to-watch-over-cats-with-a-raspberrypi/src/* ./*
```
  
Customize parameters (if needed)  
``` sh
cd cert
sudo nano iot_prov_config
```
Parameters customizable as below 
>TOPIC_MOTION (Used when installing "System-to-watch-over-cats-with-a-raspberrypi")  
TOPIC_DUST (Used when installing "System-to-watch-over-cats-with-a-raspberrypi")  
SENSOR_NO  
S3BUCKET  
PREFIX_IN1  
PREFIX_IN2 (The value is blank when not in use)  
PREFIX_IN3 (The value is blank when not in use)  
PREFIX_IN4 (The value is blank when not in use)
  
Registration of RaspberryPi as a thing to IoT core and automatic startup setting
```sh
sudo chmod u+x iot_prov.sh
./iot_prov.sh
```
  
Rewrite to your own parameters(if needed)
```sh
cd ../Camera-to-watch-over-cats-with-a-raspberrypi/template
sudo nano tmplate.yaml   
```
Parameters customizable as below  
>NameTag  
        OrgBucketName (is as same as S3BUCKET)  
        FuncName  
        Cam0 (is as same as PREFIX_IN1)  
        Cam1 (is as same as PREFIX_IN2.  Comment out Parameters and environment variables for Lambda functions when not in use)  
        Cam2 (is as same as PREFIX_IN3.  Comment out Parameters and environment variables for Lambda functions when not in use)  
        Cam3 (is as same as PREFIX_IN4.  Comment out Parameters and environment variables for Lambda functions when not in use)
  
If you want to customize the parameters, change the following directory name to the same as PREFIX_IN.  
>bed1 --> PREFIX_IN1  
bed2 --> PREFIX_IN2  
bed3 --> PREFIX_IN3  
tableside --> PREFIX_IN4
  

Also, you must change directory names (and S3 biucket name if needed ) in ./template/mimamori-project-deploy.sh.  
<br>

Modify template.yaml.  Replace "accountID" to your account ID at line 93.
```sh
sudo nano template/template.yaml
```
<br>

Deploy CloudFormation stack
```sh
sam build
sam deploy --guided --capabilities CAPABILITY_NAMED_IAM

    #Enter any stack name and [Y/N]  
        Stack Name [sam-app]: any-stack-name  
        AWS Region [ap-northeast-1]:  
        Parameter NameTag [mimamori]:  
        Parameter OrgBucketName [my-mimamori-bucket]:  
        Parameter Prefix [emr]:  
        Parameter FuncName [MyMimamoriFunc]:  
        Parameter Cam0 [bed1]:  
        Confirm changes before deploy [y/N]: Y  
        Allow SAM CLI IAM role creation [Y/n]: Y  
        Disable rollback [y/N]: y  
        Save arguments to configuration file [Y/n]: Y  
        SAM configuration file [samconfig.toml]:  
        SAM configuration environment [default]:  
        ・  
        ・  
        ・  
        Deploy this changeset? [y/N]: y
```
Confirm message like "Successfully created/updated stack - any-stack-name in ap-northeast-1"  

Open a web page with CloudFront URL
<br />
<img src="img/cloudfrontdistribution.PNG">
<br />
<br />
Select trigger for event recording
```sh
cd ..
sudo nano emr_rec.py
```
When setting the logic signal of the sensor to trigger, uncomment lines 79 and 89 then comment out lines 80 and 90.  
<br />
<img src="img/commentout_motion_detect.PNG">
<br />

When setting the motion detection of the camera to trigger, uncomment lines 80 and 90 then comment out lines 78 and 89.  
<br />
<img src="img/commentout_sensor.PNG">
<br />

Place the camera in place and restart the Raspberry Pi.  
```sh
sudo reboot
```
