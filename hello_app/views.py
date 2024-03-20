import os
from datetime import datetime
from flask import jsonify, render_template, send_from_directory, request
from . import app
from .utils import *
from .auth import auth, login_required
from .API import api
from .log_config import setup_app_logging
from .notes import notes
from .blobton import ACCOUNT, TEMP_CONTAINER, CONTAINER, blob_service

#Blueprints
app.register_blueprint(auth, url_prefix='/auth')

app.register_blueprint(api, url_prefix='/api')

app.register_blueprint(notes, url_prefix='/notes')

#Setup af logging til appen
setup_app_logging(app)

@app.route("/")
def home():
    app.logger.info("Home page requested from: %s", request.remote_addr)
    return render_template("home.html", notes = updateList(), datetime = datetime.now())

@app.route('/robots.txt')
def robots_txt():
    try:
        root_dir = os.path.abspath(os.path.dirname(__file__))
        folder_path = os.path.join(root_dir, 'static')
        app.logger.info("robots.txt requested from: %s", request.remote_addr)
        return send_from_directory(app.static_folder, 'robots.txt')
    except Exception as e:
        app.logger.error(f"Failed to serve robots.txt: {e}")
        raise
    
# Upload files to temporary container
@app.route("/upload", methods=["POST"])
def upload():
    files_list = []  # Initialize an empty list to store file dictionaries
    
    for file in request.files.getlist("file"):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fileextension = filename.rsplit('.', 1)[1]
            random_filename = id_generator() + '.' + fileextension
            ref = f'http://{ACCOUNT}.blob.core.windows.net/{TEMP_CONTAINER}/{random_filename}'
            file_dump = {
                "Type": fileextension,
                "Name": random_filename,
                "Link": ref
            }
            try:
                blob_client = blob_service.get_blob_client(container=TEMP_CONTAINER, blob=random_filename)
                blob_client.upload_blob(file)
                files_list.append(file_dump)  # Append the file dictionary to the list
            except Exception as e:
                flash('Exception=' + str(e))
                pass
    
    # Construct a list of file links
    file_links = [file['Link'] for file in files_list]
    
    # Return a JSON response containing the file links
    return jsonify({'file_links': file_links})


    
@app.route("/uploadfiles", methods=["POST"])
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
