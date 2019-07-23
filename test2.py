import face_recognition
import pickle
import numpy as np


# Load face encodings
with open('dataset_faces.dat', 'rb') as f:
    known_face_encodings = pickle.load(f)

with open('dataset_names.dat', 'rb') as f:
    known_face_names = pickle.load(f)


known_count = 0
unknown_count = 0

image = face_recognition.load_image_file("train_image.jpg")
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)
face_names = []
for face_encoding in face_encodings:
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
    face_names.append(name)
number_of_students = len(face_locations)
print(number_of_students)
print(face_names)

#    # Grab the list of names and the list of encodings
#    face_names = list(all_face_encodings.keys())
#    face_encodings = np.array(list(all_face_encodings.values()))
#
#    # Try comparing an unknown image
#    unknown_image = face_recognition.load_image_file("vallabh.jpg")
#    unknown_face = face_recognition.face_encodings(unknown_image)
#    result = face_recognition.compare_faces(face_encodings, unknown_face)
#
#    # Print the result as a list of names with True/False
#    names_with_result = list(zip(face_names, result))
#    print(names_with_result)
