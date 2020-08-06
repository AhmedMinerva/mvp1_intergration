import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from os import environ
import requests
import glob
import sys
import shutil
from flask import Flask, jsonify


#Import sqlalchemy
#from flask_sqlalchemy import SQLAlchemy
# Google Cloud Storage
bucketName = 'mvp_images'
bucketFolder = 'uploads/'

#set credentials
credential_path = "credentials.json"
environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


app = Flask(__name__)


# app.config['UPLOAD_FOLDER'] = bucketFolder
app.config['ALLOWED_EXTENSIONS'] = set([ 'png', 'jpg', 'jpeg', 'JPG'])

# storage_client = storage.Client()
# bucket = storage_client.get_bucket(bucketName)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


#files = glob.glob('cyclegan\\datasets\\dataset\\testA')
#for f in files:
    #os.remove(f)

# #can't access the folder??
# app.config['UPLOAD_FOLDER'] = "static\\uploads"

# #Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# # app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:////tmp/test.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username= db.Column(db.String(64), index=True)
#     email= db.Column(db.String(120), index=True, unique=True)
#     image_file= db.Column(db.String(120))
#     password_hash = db.Column(db.String(128))


#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"



# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    #file = request.files['file']
    if request.method == 'POST':
        file = request.files['file']
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        #src=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #file.save(src)
        dataset_pathA="static\\cyclegan\\datasets\\dataset\\testA"
        #dataset_pathB="static\\cyclegan\\datasets\\dataset\\testB"
        if os.path.isdir(dataset_pathA):
            shutil.rmtree(dataset_pathA)
            os.mkdir(dataset_pathA)
            print("emptied testA")
        test_folder_pathA=os.path.join(dataset_pathA, filename)
        #test_folder_pathB=os.path.join(dataset_pathB, filename)
        file.save(test_folder_pathA)
        # u=User(username='test1', image_file=test_folder_pathA)
        # db.session.add(u)
        # db.session.commit()
        #file.save(test_folder_pathB)
        result_path="static\\results\\selfie2anime\\test_latest\\images"
        if os.path.isdir(result_path):
            shutil.rmtree(result_path)
            os.mkdir("static\\results\\selfie2anime\\test_latest\\images")

    sys.path.insert(1, 'static\cyclegan')
    import test
    #return render_template("painter.html", image_source=os.path.join(result_path,os.listdir(result_path)[0]))
    return jsonify(os.path.join(result_path,os.listdir(result_path)[0]))



if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5000"),
        debug=True
    )
