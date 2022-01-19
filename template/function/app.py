import boto3
import os


CAM0 = os.environ['CAM0']
#CAM1 = os.environ['CAM1']
#CAM2 = os.environ['CAM2']
#CAM3 = os.environ['CAM3']
ORG_BACKET = os.environ['ORG_BACKET']

deploy_file = ["12.mp4",
                "11.mp4",
                "10.mp4",
                "09.mp4",
                "08.mp4",
                "07.mp4",
                "06.mp4",
                "05.mp4",
                "04.mp4",
                "03.mp4",
                "02.mp4",
                "01.mp4"]


def lambda_handler(event, context):
    
    for rec in event['Records']:
        filename = (rec['s3']['object']['key'])
        s3 = boto3.client('s3')

        if CAM0 in filename: dir = CAM0 + "/"
#        if CAM1 in filename: dir = CAM1 + "/"
#        if CAM2 in filename: dir = CAM2 + "/"
#        if CAM1 in filename: dir = CAM3 + "/"

        for i in range(len(deploy_file)):
            try:
                if deploy_file[i] == '01.mp4':
                    s3.copy_object(Bucket=ORG_BACKET, 
                                    Key=dir+deploy_file[i],
                                    CopySource={'Bucket': ORG_BACKET, 
                                                'Key': filename})
                    s3.delete_object(Bucket=ORG_BACKET, 
                                    Key=filename)
                    break
                s3.copy_object(Bucket=ORG_BACKET, 
                                    Key=dir+deploy_file[i], 
                                    CopySource={'Bucket': ORG_BACKET, 
                                                'Key': dir+deploy_file[i+1]})
            except Exception as e:
                pass