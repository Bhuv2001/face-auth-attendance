# face-auth-attendance
Face Authentication Attendance System automates attendance using facial recognition. It registers users, extracts face embeddings, and performs real-time authentication via camera input. The system supports smart punch-in/punch-out, prevents duplicate entries, logs attendance in CSV format, and is deployed as a Streamlit web app.
# Face Authentication Attendance System

## 📌 Overview
The **Face Authentication Attendance System** is a computer vision–based application that automates attendance marking using facial recognition.  
Instead of manual registers or ID cards, the system authenticates users through their face and records attendance automatically with smart punch-in and punch-out logic.

The project is deployed as a **Streamlit web application**, allowing browser-based camera access and a live, shareable demo link.

---

## 🚀 Features
- Face registration and recognition
- Real-time face authentication
- Automatic Punch-In and Punch-Out
- Smart toggle to avoid duplicate entries
- Attendance stored in CSV format
- Browser-based camera support (Streamlit)
- Easy deployment and sharing

---

## 🧠 How It Works
1. User captures their face using a camera.
2. Facial features are extracted as embeddings using a deep learning model.
3. Live images are compared against stored embeddings.
4. On successful recognition:
   - First detection → **IN time**
   - Next detection after a time gap → **OUT time**
5. Attendance is logged automatically in a CSV file.

---

## 🗂️ Project Structure

---

## 🛠️ Technologies Used
- Python 3.11
- OpenCV
- face_recognition (dlib)
- NumPy
- Streamlit
- CSV for data storage

---

## ▶️ Running Locally
```bash
source venv/bin/activate
streamlit run app.py
