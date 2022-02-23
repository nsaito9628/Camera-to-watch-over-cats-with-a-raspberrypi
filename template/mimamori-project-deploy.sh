#!/bin/bash

BUCKET_NAME=$(cat ../../iot_prov_config | grep S3BUCKET | awk -F'=' '{print $2}')

pip3 install -U awscli
/usr/local/bin/aws s3 cp ./index.html s3://${BUCKET_NAME}
/usr/local/bin/aws s3 cp ./css/ s3://${BUCKET_NAME}/css --recursive
/usr/local/bin/aws s3 cp ./bed1/ s3://${BUCKET_NAME}/bed1 --recursive
#/usr/local/bin/aws s3 cp ./bed2/ s3://${BUCKET_NAME}/bed2 --recursive
#/usr/local/bin/aws s3 cp ./bed3/ s3://${BUCKET_NAME}/bed3 --recursive
#/usr/local/bin/aws s3 cp ./tableside/ s3://${BUCKET_NAME}/tableside --recursive
/usr/local/bin/aws s3 cp ./img/ s3://${BUCKET_NAME}/img --recursive

exit 0