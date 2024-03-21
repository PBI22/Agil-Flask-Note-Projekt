from azure.storage.blob import BlobServiceClient
import os

ACCOUNT = 'flasknoteblobstorage' # Azure account name
TEMP_CONTAINER = "tempimages" # Container name
CONTAINER = "images" # Container name
import os
from azure.storage.blob import BlobServiceClient

conn_str = os.environ.get('BLOB_CONNECTION_STRING')
if conn_str:
    blob_service = BlobServiceClient.from_connection_string(conn_str=conn_str)
else:
    # Handle the case where the environment variable is not set
    print("BLOB_CONNECTION_STRING environment variable is not set.")

blob_service = BlobServiceClient.from_connection_string(conn_str=conn_str)