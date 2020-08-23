import boto3
import json
import logging
import os

s3 = boto3.client('s3')
response = s3.list_buckets()
 


# Output the bucket names
bkt={}
def getbucket():
 count=0
 print('Existing buckets:')
 for bucket in response['Buckets']:
         count+=1
         print(f'bucket name is  {bucket["Name"]}')
         bkt[count]=bucket["Name"]

#  print(f"the bucket dict is {bkt}")


def lambda_handler(event, context):
 dynamodb = boto3.resource('dynamodb')
 table = dynamodb.Table('mytable')
 getbucket()
#  table.put_item(
#   Item={
#         'username': 'janedoe',
#         'first_name': 'Jane',
#         'last_name': 'Doe',
#         'id': 25,
#         'account_type': 'standard_user',
#     }
# )
 try:
    for key, values in bkt.items():
        table.put_item(Item={
            'id': key,
            "bname":values
            }
            )
 except:
     print("values could not be inserted\n")
     
     
 print("all values were inserted successfully\n")
 resp=json.dumps({
     "status":200,
     "message":"sucess"
 })
 
 return resp


   

