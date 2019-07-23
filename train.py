import face_recognition
import pickle


all_face_encodings = {}

img1 = face_recognition.load_image_file("vallabh.jpg")
all_face_encodings["vallabh"] = face_recognition.face_encodings(img1)[0]

img2 = face_recognition.load_image_file("mangesh.jpg")
all_face_encodings["mangesh"] = face_recognition.face_encodings(img2)[0]

# ... etc ...

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)
