from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .utils import *
from .blobton import ACCOUNT, CONTAINER, TEMP_CONTAINER, blob_service
import os

dam = Blueprint('dam', __name__)
    
# Function to generate a random filename
def generate_random_filename():
    return os.urandom(16).hex()

# Global variable to store generated filenames
generated_filenames = []

@dam.route("/upload", methods=["POST"])
def upload():
    global generated_filenames  # Access the global variable
    files_list = []  # Initialize an empty list to store file dictionaries
    filenames = []   # Initialize an empty list to store generated filenames
    
    for file in request.files.getlist("file"):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fileextension = filename.rsplit('.', 1)[1]
            random_filename = generate_random_filename()
            filename = f"{random_filename}.{fileextension}"
            ref = f'http://{ACCOUNT}.blob.core.windows.net/{TEMP_CONTAINER}/{filename}'
            file_dump = {
                "Type": fileextension,
                "Name": filename,
                "Link": ref
            }
            try:
                blob_client = blob_service.get_blob_client(container=TEMP_CONTAINER, blob=filename)
                blob_client.upload_blob(file)
                files_list.append(file_dump)  # Append the file dictionary to the list
                filenames.append(filename)   # Append the generated filename to the list
            except Exception as e:
                flash('Exception=' + str(e))
                pass
    
    # Store generated filenames globally
    generated_filenames = filenames
    
    # Construct a list of file links
    file_links = [file['Link'] for file in files_list]
    
    # Return a JSON response containing the file links and filenames
    return jsonify({'file_links': file_links, 'filenames': filenames})


@dam.route("/uploadfiles", methods=["POST"])
def uploadfiles():
    global generated_filenames  # Access the global variable
    persistent_files_list = []  # Initialize an empty list to store file dictionaries
    filenames = generated_filenames  # Use the filenames generated in upload() function
    
    for file, filename in zip(request.files.getlist("file"), filenames):
        if file and allowed_file(file.filename):
            filename = secure_filename(filename)
            fileextension = filename.rsplit('.', 1)[1]
            ref = 'http://' + ACCOUNT + '.blob.core.windows.net/' + CONTAINER + '/' + filename
            file_dump = {
                "Type": fileextension,
                "Name": filename,
                "Link": ref
            }
            try:
                blob_client = blob_service.get_blob_client(container=CONTAINER, blob=filename)
                blob_client.upload_blob(file)
                persistent_files_list.append(file_dump)  # Append the file dictionary to the list
            except Exception as e:
                flash('Exception=' + str(e))
                pass
    
    # Construct a list of file links
    file_links = [file['Link'] for file in persistent_files_list]
    
    # Return a JSON response containing the file links
    return jsonify({'file_links': file_links})

