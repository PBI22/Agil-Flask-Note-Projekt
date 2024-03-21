from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from azure.storage.blob import BlobServiceClient, BlobClient
import os

# Initialize Azure Blob Service Client
account = 'flasknoteblobstorage'   # Azure account name
tempcontainer = "tempimages" # Container name
connection_string = os.environ.get("CONNECTION_STRING")

# "DefaultEndpointsProtocol=https;AccountName=flasknoteblobstorage;AccountKey=BnJBe5WkjWApSRwguDmueGabw3+WZmnIE3GwjfnMezNM1Td+xO8TdrHKQiDGyomo7ZBxGjGIQuiJ+AStd6P1kA==;EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_client = blob_service_client.get_container_client(tempcontainer)

# Function to delete images older than 24 hours from Azure Blob Storage Temporary Image container
def delete_old_images():
    current_time = datetime.now(timezone.utc)
    threshold_time = current_time - timedelta(hours=1)

    # List all blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        blob_client = BlobClient.from_connection_string(connection_string, tempcontainer, blob.name)
        blob_properties = blob_client.get_blob_properties()
        
        creation_time = blob_properties.creation_time
        if creation_time <= threshold_time:
            # Delete the blob from the container
            container_client.delete_blob(blob.name)
            print("Deleted blob '{}' created at {}".format(blob.name, creation_time))

# Create and start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_images, 'interval', hours=0.001)  # Run every hour
scheduler.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    scheduler.shutdown()