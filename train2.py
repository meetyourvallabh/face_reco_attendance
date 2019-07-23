import face_recognition
import pickle


known_face_encodings = []
known_name = ["vallabh", "mangesh"]

img1 = face_recognition.load_image_file("vallabh.jpg")
known_face_encodings.append(face_recognition.face_encodings(img1)[0])

img2 = face_recognition.load_image_file("mangesh.jpg")
known_face_encodings.append(face_recognition.face_encodings(img2)[0])


# ... etc ...

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(known_face_encodings, f, pickle.HIGHEST_PROTOCOL)

with open('dataset_names.dat', 'wb') as d:
    pickle.dump(known_name, d)


print(known_face_encodings)
print(known_name)
