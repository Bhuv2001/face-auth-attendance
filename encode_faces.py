import face_recognition
import os
import pickle

dataset_path = "dataset"
known_encodings = []
known_names = []

for person in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person)

    if not os.path.isdir(person_path):
        continue

    for img in os.listdir(person_path):
        # ✅ Ignore hidden/system files
        if img.startswith('.'):
            continue

        img_path = os.path.join(person_path, img)

        try:
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person)
        except Exception as e:
            print(f"Skipping file {img_path}: {e}")

os.makedirs("encodings", exist_ok=True)
with open("encodings/encodings.pkl", "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("✅ Face encodings saved successfully")
