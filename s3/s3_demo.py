import pprint

import boto3
from botocore.exceptions import ClientError, BotoCoreError



# # connecting to s3
# try:
#     s3_client = boto3.client('s3')
#     print('Successfully connected to s3 client')
# except ClientError as e:
#     print('Error connecting to s3 client', e)
#
# # # list buckets
# response = s3_client.list_buckets()
# pprint.pprint(response)
# #
# #
# # # credentials
# #
# #
# # # Output the bucket names
# print('Existing buckets:')
# for bucket in response['Buckets']:
#     print(f'  {bucket["Name"]}')


# creating resource
# s3 = boto3.resource('s3')
# print("Listing buckets using resource")
# for bucket in s3.buckets.all():
#     print(bucket)



# # get specific bucket and list it's objects
# my_csv_file = None
# s3 = boto3.resource('s3')
# # my_bucket = s3.Bucket('valeria123')
# my_bucket = s3.Bucket('edulabs-public')
# for obj in my_bucket.objects.all():
#     print(obj)
#     if obj.key.endswith('.csv'):
#         my_csv_file = obj.key
#         print("found csv: ", my_csv_file)



# download file
# s3 = boto3.client('s3')
# # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
# s3.download_file('edulabs-public', 'concap.csv', 'temp.csv')
# print(f"downloaded to temp.csv")

# as stream
# with open('temp.csv', 'wb') as f:
#     s3.download_fileobj('edulabs-public', 'concap.csv', f)


#
# # as stream - user resource
# file_obj = s3.Object('valeria123', my_csv_file)
# file_content = file_obj.get()['Body'].read()

# print(f"file content (as bytestring): {file_content}")
# decode
# decoded = file_content.decode()
# print(f"file content (as string) - decoded: {decoded}")

# line by line
# file_obj = s3.Object('valeria123', my_csv_file)
# for i, line in enumerate(file_obj.get()['Body'].iter_lines()):
#     print(f"Line {i}: ", line.decode())




# upload file
# s3 = boto3.client('s3')
# response = s3.upload_file('requirements.txt', 'edulabs-private', 'a/b/c/d/requirements.txt')
# print('Successfully uploaded')

# need to add write permissions



# secrets_client = boto3.client('secretsmanager', region_name = "us-east-1")
# response = secrets_client.get_secret_value(SecretId='mysecret')
# print("done")