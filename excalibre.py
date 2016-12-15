#!/usr/bin/env python

import os

import subprocess

from flask import Flask, abort, request, send_from_directory, redirect, render_template, url_for

from werkzeug.utils import secure_filename

EBOOK_CONVERT = 'ebook-convert'
UPLOAD_FOLDER = '/var/uploads'
ALLOWED_EXTENSIONS = set(['rtf'])

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/conversions/', methods = ['GET', 'POST'])
def conversions():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.files:
        file = request.files.get('file') # 'file' is the name attribute of the <input type="file" name="file"> element
        if file:
            filename = file.filename.strip()
            if allowed_file(filename):
                filename = secure_filename(filename)
                assert filename
                absolute_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                absolute_result_filename = "{0}.MOBI".format(os.path.splitext(absolute_filename)[0])
                assert absolute_result_filename
                file.save(absolute_filename)
                
                subprocess.check_call([app.config['EBOOK_CONVERT'], absolute_filename, absolute_result_filename])

                return redirect(url_for('conversion', filename=os.path.basename(absolute_result_filename)))
    abort(500)
        
@app.route('/conversions/<filename>', methods = ['GET'])
def conversion(filename):
    # TODO: figure out some way to delete it.  There's arcane Flask
    # stuff that might be able to delete it after the request closes,
    # but I'm too stupid to figure out what that is right now.
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
def allowed_file(filename):
    return filename and \
        '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

