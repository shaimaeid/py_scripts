import boto3
from botocore.exceptions import NoCredentialsError
from myapi.logger import mylogger

# Replace these values with your own AWS credentials
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

# Create a boto3 client
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)



def upload_to_s3(file_path, object_name=None):
    if object_name is None:
        object_name = file_path
   
    try:
        response = s3_client.upload_file(file_path, BUCKET_NAME, "realestate_templates/videos/"+object_name)
    except FileNotFoundError:
        mylogger.error("FileNotFoundError")
        return False
    except NoCredentialsError:
        mylogger.error("NoCredentialsError")
        return False
    except Exception as e:
        mylogger.error(e)

    mylogger.error(response , type(response))

    if(response is False):
        mylogger.error("File upload error")
        return False  
    else:
       return f"https://{BUCKET_NAME}.s3.amazonaws.com/videos/"+object_name
    
def download_file_from_s3(object_name, file_path):
    """
    Download a file from an S3 bucket

    :param bucket_name: S3 bucket name
    :param object_name: S3 object name (key)
    :param file_path: Local path where the file will be downloaded
    :return: True if file was downloaded successfully, else False
    """
    try:
        s3_client.download_file(BUCKET_NAME, object_name, file_path)
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False