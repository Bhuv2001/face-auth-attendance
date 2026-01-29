import cv2
import os

name = input("Enter user name: ")
path = f"dataset/{name}"

if not os.path.exists(path):
    os.makedirs(path)

cam = cv2.VideoCapture(0)
count = 0

print("Press S to save image, Q to quit")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):
        count += 1
        cv2.imwrite(f"{path}/{count}.jpg", frame)
        print(f"Saved image {count}")

    elif key == ord('q') or count >= 10:
        break

cam.release()
cv2.destroyAllWindows()
