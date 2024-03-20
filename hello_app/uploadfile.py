from flask import Blueprint, jsonify, request, flash
from .utils import *
from .blobton import ACCOUNT, CONTAINER, blob_service

uploadfile = Blueprint('uploadfile', __name__)

# Upload files to final container
@uploadfile.route("/uploadfiles", methods=["POST"])
def uploadfiles():
    persistent_files_list = []  # Initialize an empty list to store file dictionaries
    filenames = request.form.getlist("filename")  # Get the filenames
    
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
