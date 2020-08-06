import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask import send_file
#  To load the image from url
from PIL import Image
import requests
from io import BytesIO
import numpy as np
#import cv2
# To cartoonify
#from model.main_model import cartoonize
from werkzeug.utils import secure_filename
from os import environ
import glob
import sys
import shutil


app = Flask(__name__)


@app.route('/api', methods=['POST'])
def convert_image():

    # Load image
    try:
        url = request.args['url']
    except:
        return jsonify('No url specified')
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    dataset_pathA="static\\cyclegan\\datasets\\dataset\\testA"
    #dataset_pathB="static\\cyclegan\\datasets\\dataset\\testB"
    if os.path.isdir(dataset_pathA):
        shutil.rmtree(dataset_pathA)
        os.mkdir(dataset_pathA)
        print("emptied testA")
    extension = url.split('/')[-1].split('.')[1]
    test_folder_pathA=os.path.join(dataset_pathA,'img.'+extension)
    #test_folder_pathB=os.path.join(dataset_pathB, filename)
    img.save(test_folder_pathA)
    result_path="static\\results\\selfie2anime\\test_latest\\images"
    if os.path.isdir(result_path):
        shutil.rmtree(result_path)
        os.mkdir("static\\results\\selfie2anime\\test_latest\\images")

    sys.path.insert(1,'static\cyclegan')
    import test
    img=Image.open(os.path.join(result_path,os.listdir(result_path)[0]))
    out = np.array(img)
    answer = {'img_bits': list(out.flatten().tolist()),
          'dim': out.shape}
    return jsonify(answer)

    # # Convert image to CV2 to use it on model
    # open_cv_image = np.array(img) 
    # open_cv_image = open_cv_image[:, :, ::-1].copy() 

    # # Cartoonify
    # out = cartoonize(open_cv_image)
    # # Prepare answer and return
    # answer = {'img_bits': list(out.flatten().tolist()),
    #           'dim': out.shape}
    # return jsonify(answer)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

