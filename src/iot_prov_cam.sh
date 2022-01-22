#!/bin/bash

#/home/pi/ --> mkdir cert && cd cert && cp iot_prov.sh
sudo apt install jq -y
sudo apt update -y
sudo apt upgrade -y

crontab -r

# creating cron_mod.conf
echo >> ./cron_mod.conf
echo HOST_ENDPOINT="dummy" >> cron_mod.conf
echo CACERT="dummy" >> cron_mod.conf
echo CLIENTCERT="dummy" >> cron_mod.conf
echo CLIENTKEY="dummy" >> cron_mod.conf
echo >> cron_mod.conf
echo TOPIC_MOTION="dummy" >> cron_mod.conf
echo TOPIC_DUST="dummy" >> cron_mod.conf
echo >> cron_mod.conf
echo ACCESS_KEY=$(cat ./.aws/credentials | grep aws_access_key_id | awk -F'= ' '{print $2}') >> ./cron_mod.conf
echo SECRET_KEY=$(cat ./.aws/credentials | grep aws_secret_access_key | awk -F'= ' '{print $2}') >> ./cron_mod.conf
echo REGION=$(cat ./.aws/config | grep region | awk -F'= ' '{print $2}') >> ./cron_mod.conf
echo SENSOR_NO=$(cat ./iot_prov_config | grep SENSOR_NO | awk -F'=' '{print $2}') >> ./cron_mod.conf
echo S3BUCKET=$(cat ./iot_prov_config | grep S3BUCKET | awk -F'=' '{print $2}') >> ./cron_mod.conf
echo
if [[ $(cat ./iot_prov_config | grep PREFIX_IN1 | awk -F'=' '{print $2}') != "" ]]; then
    echo PREFIX_IN1=$(cat ./iot_prov_config | grep PREFIX_IN1 | awk -F'=' '{print $2}') >> ./cron_mod.conf
    else
    : #pass
    fi
if [[ $(cat ./iot_prov_config | grep PREFIX_IN2 | awk -F'=' '{print $2}') != "" ]]; then
    echo PREFIX_IN2=$(cat ./iot_prov_config | grep PREFIX_IN2 | awk -F'=' '{print $2}') >> ./cron_mod.conf
    else
    : #pass
    fi
if [[ $(cat ./iot_prov_config | grep PREFIX_IN3 | awk -F'=' '{print $2}') != "" ]]; then
    echo PREFIX_IN3=$(cat ./iot_prov_config | grep PREFIX_IN3 | awk -F'=' '{print $2}') >> ./cron_mod.conf
    else
    : #pass
    fi
if [[ $(cat ./iot_prov_config | grep PREFIX_IN4 | awk -F'=' '{print $2}') != "" ]]; then
    echo PREFIX_IN4=$(cat ./iot_prov_config | grep PREFIX_IN4 | awk -F'=' '{print $2}') >> ./cron_mod.conf
    else
    : #pass
    fi

echo >> ./cron_mod.conf
if [ ! -e /home/pi/overclock.sh ]; then
    echo
    else 
    echo @reboot sudo sh /home/pi/overclock.sh >> ./cron_mod.conf
    fi

echo >> ./cron_mod.conf

if [ ! -e /home/pi/emr_rec.py ]; then
    echo
    else 
    echo @reboot python /home/pi/emr_rec.py >> ./cron_mod.conf
    fi


# adding .profile
echo >> ./.profile
echo HOST_ENDPOINT="dummy" >> ./.profile
echo CACERT="dummy" >> ./.profile
echo CLIENTCERT="dummy" >> ./.profile
echo CLIENTKEY="dummy" >> ./.profile
echo >> ./.profile
echo TOPIC_MOTION="dummy" >> ./.profile
echo TOPIC_DUST="dummy" >> ./.profile
echo >> ./.profile
echo export ACCESS_KEY=$(cat ./.aws/credentials | grep aws_access_key_id | awk -F'= ' '{print $2}') >> ./.profile
echo export SECRET_KEY=$(cat ./.aws/credentials | grep aws_secret_access_key | awk -F'= ' '{print $2}') >> ./.profile
echo export REGION=$(cat ./.aws/config | grep region | awk -F'= ' '{print $2}') >> ./.profile
echo export SENSOR_NO=$(cat ./iot_prov_config | grep SENSOR_NO | awk -F'=' '{print $2}') >> ./.profile
echo export S3BUCKET=$(cat ./iot_prov_config | grep S3BUCKET | awk -F'=' '{print $2}') >> ./.profile
if [[ $(cat ./iot_prov_config | grep PREFIX_IN1 | awk -F'=' '{print $2}') != "" ]]; then
    echo export PREFIX_IN1=$(cat ./iot_prov_config | grep PREFIX_IN1 | awk -F'=' '{print $2}') >> ./.profile
    else
    : #pass
    fi
if [[ $(cat ./iot_prov_config | grep PREFIX_IN2 | awk -F'=' '{print $2}') != "" ]]; then
    export echo PREFIX_IN2=$(cat ./iot_prov_config | grep PREFIX_IN2 | awk -F'=' '{print $2}') >> ./.profile
    else
    : #pass
    fi
if [[ $(cat ./iot_prov_config | grep PREFIX_IN3 | awk -F'=' '{print $2}') != "" ]]; then
    export echo PREFIX_IN3=$(cat ./iot_prov_config | grep PREFIX_IN3 | awk -F'=' '{print $2}') >> ./.profile
    else
    : #pass
    fi
if [[ $(cat ./iot_prov_config | grep PREFIX_IN4 | awk -F'=' '{print $2}') != "" ]]; then
    export echo PREFIX_IN4=$(cat ./iot_prov_config | grep PREFIX_IN4 | awk -F'=' '{print $2}') >> ./.profile
    else
    : #pass
    fi

crontab ./cron_mod.conf