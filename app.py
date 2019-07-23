from flask import Flask, render_template, request, flash, redirect, url_for, session, json, jsonify, make_response, send_from_directory
import os
import requests
import datetime
from flask_pymongo import PyMongo
import face_recognition
from flask_mail import Mail, Message
import pickle
from PIL import Image

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['pdf', 'docx', 'doc'])
UPLOAD_DIRECTORY = "/static/"

app.config['MONGO_DBNAME'] = 'vdjobs'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/vdjobs'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'developer@makeyourown.club'
app.config['MAIL_PASSWORD'] = 'myocoo@123'
#UPLOAD_FOLDER = os.path.abspath('/static/img')
#app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
mongo = PyMongo(app)
mail = Mail(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    x = str(datetime.datetime.now())[:10]
    print(x)
    return render_template("index.html")


@app.route('/capture', methods=['POST', 'GET'])
def capture():
    return render_template("capture.html")


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        x = str(datetime.datetime.now())[:10]
        path = os.path.abspath('static/attendance/')
        if not os.path.exists(path):
            os.makedirs(path)
        app.config['UPLOAD_FOLDER'] = path
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if request.method == 'POST':
            file = request.files['image']
            f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            print(path+file.filename)
            final_path = path+'/'+file.filename
            file.save(f)
            session['image_path'] = final_path
            return redirect(url_for('result'))

    return render_template("upload.html")


@app.route('/result', methods=['GET', 'POST'])
def result():
    known_count = 0
    unknown_count = 0
    vallabh_image = face_recognition.load_image_file("vallabh.jpg")
    vallabh_face_encoding = face_recognition.face_encodings(vallabh_image)[0]
    mangesh_image = face_recognition.load_image_file("mangesh.jpg")
    mangesh_face_encoding = face_recognition.face_encodings(mangesh_image)[0]

    shreya_image = face_recognition.load_image_file("shreya.jpg")
    shreya_face_encoding = face_recognition.face_encodings(shreya_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        vallabh_face_encoding,
        mangesh_face_encoding,
        shreya_face_encoding
    ]
    known_face_names = [
        "Vallabh Hake",
        "Mangesh Patil",
        "Shreya Wani"
    ]

    # with open('dataset_faces.dat', 'rb') as f:
    #    known_face_encodings = pickle.load(f)
#
    # with open('dataset_names.dat', 'rb') as f:
    #    known_face_names = pickle.load(f)
#
    final_path = session['image_path']
    image = face_recognition.load_image_file(final_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    face_names = []

    for face_encoding, face_location in zip(face_encodings, face_locations):
            # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding, 0.5)
        name = "Unknown"
        #distance = face_recognition.face_distance(known_face_encodings, face_encoding)

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            known_count = known_count+1
        else:
            unknown_count = unknown_count+1

            top, right, bottom, left = face_location
            print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(
                top, left, bottom, right))
            face_image = image[top-100:bottom+100, left-100:right+100]
            pil_image = Image.fromarray(face_image)
            pil_image.show()

        face_names.append(name)

    number_of_students = len(face_locations)
    # print(number_of_students)
    os.remove(final_path)
    session['image_path'] = ''
    return render_template('result.html', number_of_students=number_of_students, face_names=face_names, known_count=known_count, unknown_count=unknown_count)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host='0.0.0.0', debug='true', port='5000')
