import cv2
import face_recognition
import pickle
import csv
import os
from datetime import datetime, timedelta
from spoof_check import is_real_face

MIN_GAP = timedelta(minutes=2)
ATTENDANCE_FILE = "/Users/navneetsingh/Desktop/face_attendace/attendance.csv"

with open("encodings/encodings.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

def read_attendance():
    records = []
    if not os.path.exists(ATTENDANCE_FILE):
        return records

    with open(ATTENDANCE_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records

def write_attendance(records):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Date", "In", "Out"])
        writer.writeheader()
        writer.writerows(records)

def mark_attendance(name):
    print("mark_attendance() called for", name)
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now()

    records = read_attendance()

    for row in records:
        if row["Name"] == name and row["Date"] == today:
            if row["Out"] == "":
                in_time = datetime.strptime(row["In"], "%H:%M:%S")
                if now - in_time >= MIN_GAP:
                    row["Out"] = now.strftime("%H:%M:%S")
                    write_attendance(records)
                    print(f"OUT marked for {name}")
            return

    records.append({
        "Name": name,
        "Date": today,
        "In": now.strftime("%H:%M:%S"),
        "Out": ""
    })
    write_attendance(records)
    print(f"IN marked for {name}")

cam = cv2.VideoCapture(0)
marked_recently = {}

print("Press Q to quit")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for encoding, loc in zip(encodings, locations):
        matches = face_recognition.compare_faces(known_encodings, encoding, 0.5)
        name = "Unknown"

        if True in matches:
            idx = matches.index(True)
            name = known_names[idx]

            if is_real_face(frame):
                last_seen = marked_recently.get(name)
                if not last_seen or datetime.now() - last_seen > timedelta(seconds=30):
                    mark_attendance(name)
                    marked_recently[name] = datetime.now()

        top, right, bottom, left = loc
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Smart Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
