import streamlit as st
import face_recognition
import pickle
import csv
import os
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import cv2

# ---------------- CONFIG ----------------
ATTENDANCE_FILE = "attendance.csv"
MIN_GAP = timedelta(minutes=2)   # change to seconds for quick demo
# ----------------------------------------

st.set_page_config(page_title="Face Attendance System", layout="centered")
st.title("📸 Face Authentication Attendance System")

# --------- Load face encodings ----------
if not os.path.exists("encodings/encodings.pkl"):
    st.error("❌ encodings.pkl not found. Run encode_faces.py first.")
    st.stop()

with open("encodings/encodings.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

# ---------- Attendance helpers ----------
def read_attendance():
    records = []
    if os.path.exists(ATTENDANCE_FILE):
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
                    return "OUT marked"
            return "Already marked"

    records.append({
        "Name": name,
        "Date": today,
        "In": now.strftime("%H:%M:%S"),
        "Out": ""
    })
    write_attendance(records)
    return "IN marked"

# -------- Camera input (Streamlit) -------
image = st.camera_input("Capture your face")

if image is not None:
    # Convert image safely for dlib
    img = Image.open(image).convert("RGB")
    frame = np.array(img, dtype=np.uint8)
    frame = np.ascontiguousarray(frame)

    # Face detection
    locations = face_recognition.face_locations(frame, model="hog")

    if not locations:
        st.error("❌ No face detected. Try better lighting.")
        st.stop()

    # Face encoding (SAFE)
    encodings = face_recognition.face_encodings(frame, locations)

    if not encodings:
        st.error("❌ Face encoding failed. Try again.")
        st.stop()

    encoding = encodings[0]

    # Compare faces
    matches = face_recognition.compare_faces(
        known_encodings,
        encoding,
        tolerance=0.5
    )

    if True in matches:
        idx = matches.index(True)
        name = known_names[idx]

        result = mark_attendance(name)
        st.success(f"✅ {name} recognized — {result}")

    else:
        st.error("❌ Face not recognized")

# --------- Show attendance table ---------
st.divider()
st.subheader("📄 Attendance Records")

records = read_attendance()
if records:
    st.dataframe(records)
else:
    st.info("No attendance records yet.")
