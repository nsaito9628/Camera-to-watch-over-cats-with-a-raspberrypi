#!/bin/bash

pip3 install -U awscli
/usr/local/bin/aws s3 cp ./index.html s3://my-mimamori-bucket
/usr/local/bin/aws s3 cp ./css/ s3://my-mimamori-bucket/css --recursive
/usr/local/bin/aws s3 cp ./bed1/ s3://my-mimamori-bucket/bed1 --recursive
#/usr/local/bin/aws s3 cp ./bed2/ s3://my-mimamori-bucket/bed2 --recursive
#/usr/local/bin/aws s3 cp ./bed3/ s3://my-mimamori-bucket/bed3 --recursive
#/usr/local/bin/aws s3 cp ./tableside/ s3://my-mimamori-bucket/tableside --recursive
/usr/local/bin/aws s3 cp ./img/ s3://my-mimamori-bucket/img --recursive

exit 0