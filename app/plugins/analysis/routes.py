"""AUCR analysis plugin default flask app blueprint routes."""
# coding=utf-8
import os
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.analysis.file.upload import create_upload_file
from app.plugins.analysis.models import AnalysisPlugins

analysis_page = Blueprint('analysis', __name__, template_folder='templates')


def allowed_file(filename):
    """Return filename if allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@analysis_page.route('', methods=['GET'])
@login_required
def analysis():
    """Return AUCR analysis plugin flask app analysis blueprint."""
    analysis_info = AnalysisPlugins.query.all()
    return render_template('analysis.html', title='Analysis', analysis_info=analysis_info)


@analysis_page.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    """Return File Upload flask app analysis blueprint."""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file, or that file type is not supported')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_hash = create_upload_file(file, os.path.join(current_app.config['FILE_FOLDER']))
            flash("The " + str(filename) + " md5:" + file_hash + " has been uploaded!")
    return render_template('upload_file.html', title='Upload File')
