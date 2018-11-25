import logging
import os
import boto3


# enabloe logging messages to airflow
log = logging.getLogger(__name__)
# store staging directory in the AIRFLOW_HOME
local_dir = os.getcwd()


class Load:

	@classmethod
	def upload_to_S3(cls, **context):
		
		storage_name = context['params']['base']
		base = os.path.join(local_dir, storage_name)
		bucket_name = 'storeweather'

		session = boto3.Session(
			aws_access_key_id='',
			aws_secret_access_key='',
			region_name='us-east-1'
		)
		s3 = session.resource('s3')
		bucket = s3.Bucket(bucket_name)
		
		log.info("Getting Bucket Name")
		log.info(bucket)

		for subdir, dirs, files in os.walk(base):
			for file in files:
				full_path = os.path.join(subdir, file)
				with open(full_path, 'rb') as data:
					bucket.put_object(Key=full_path[len(base)+1:], Body=data)