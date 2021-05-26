from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from image import ImageScanning
import os

app=Flask(__name__)

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'jpg', 'png','jpeg'}

def allowed_file(filename):
    # does the file have extension
    # is the extension allowed one
    return '.' in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=["POST","GET"])
def upload_form():
    if request.method == "POST":
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(filepath)
            im = ImageScanning(filepath)
            return jsonify(im.extrackArgs())
            os.remove(filepath)
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''
           
