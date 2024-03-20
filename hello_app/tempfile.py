import markdown2
import json
import os
from datetime import datetime
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session
from . import app
from .models import Note
from .utils import *
from .blobton import ACCOUNT, TEMP_CONTAINER, blob_service

tempfile = Blueprint('tempfile', __name__)

# Upload files to temporary container
@tempfile.route("/upload", methods=["POST"])
def upload():
    files_list = []  # Initialize an empty list to store file dictionaries
    filenames = request.form.getlist('filenames')  # Get the filenames
    
    for file, filename in zip(request.files.getlist("file"), filenames):
        if file and allowed_file(file.filename):
            filename = secure_filename(filename)
            fileextension = filename.rsplit('.', 1)[1]
            ref = 'http://' + ACCOUNT + '.blob.core.windows.net/' + TEMP_CONTAINER + '/' + filename
            file_dump = {
                "Type": fileextension,
                "Name": filename,
                "Link": ref
            }
            try:
                blob_client = blob_service.get_blob_client(container=TEMP_CONTAINER, blob=filename)
                blob_client.upload_blob(file)
                files_list.append(file_dump)  # Append the file dictionary to the list
            except Exception as e:
                flash('Exception=' + str(e))
                pass
    
    # Construct a list of file links
    file_links = [file['Link'] for file in files_list]
    
    # Return a JSON response containing the file links
    return jsonify({'file_links': file_links})
