from azure.storage.blob import BlobServiceClient
import os

ACCOUNT = 'flasknoteblobstorage'   # Azure account name
TEMP_CONTAINER = "tempimages" # Container name
CONTAINER = "images" # Container name
CONNECTION_STRING = os.environ.get('CONNECTION_STRING')
blob_service = BlobServiceClient.from_connection_string(conn_str=CONNECTION_STRING)