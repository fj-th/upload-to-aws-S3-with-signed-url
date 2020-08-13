#from https://qiita.com/tsukuba_japan/items/00266727b64e1167c4f3
import boto3
from botocore.client import Config
import json
import uuid

def lambda_handler(event, context):

    PUT_BUCKET = 's3 bucket' #S3バケット名
    UUID = str(uuid.uuid4()) #uuid(一意に識別するためのランダム値)を発行
    PUT_KEY = 'put_folder/' + UUID #S3にアップロードされるファイルの保存名を決定(uuidを用いて重複を避ける)

    BORROW_TIME = 300  #URLの有効期限(sec)

    #region_nameはS3のリージョン名(東京リージョンなら'ap-northeast-1')
    s3 = boto3.client('s3', region_name='region_name', config=Config(signature_version='s3v4'))

    s3.put_object(
        Bucket=PUT_BUCKET,
        Key=PUT_KEY
    )

    put_url = s3.generate_presigned_url(
        ClientMethod = 'put_object', 
        Params = {'Bucket' : PUT_BUCKET, 'Key' : PUT_KEY}, 
        ExpiresIn = BORROW_TIME, 
        HttpMethod = 'PUT')

    #body要素にjsonを与えると、GETリクエストに対してよしなにjsonを返してくれる
    return {
        'statusCode': 200,
        'headers': {
        "Access-Control-Allow-Origin": "*"
        },
        'isBase64Encoded': False,
        'body': json.dumps(
            {
                'PUT_URL': put_url,
                'UUID': UUID
            }
        )
    }