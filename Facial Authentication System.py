Requirement already satisfied: flask in c:\users\vinay\anaconda3\lib\site-packages 
(2.2.2)
Requirement already satisfied: opencv-python in c:\users\vinay\anaconda3\lib\site
packages (4.12.0.88)
Requirement already satisfied: imutils in c:\users\vinay\anaconda3\lib\site-packag
es (0.5.4)
Requirement already satisfied: Werkzeug>=2.2.2 in c:\users\vinay\anaconda3\lib\sit
e-packages (from flask) (2.2.3)
Requirement already satisfied: Jinja2>=3.0 in c:\users\vinay\anaconda3\lib\site-pa
ckages (from flask) (3.1.2)
Requirement already satisfied: itsdangerous>=2.0 in c:\users\vinay\anaconda3\lib\s
ite-packages (from flask) (2.0.1)
Requirement already satisfied: click>=8.0 in c:\users\vinay\anaconda3\lib\site-pac
kages (from flask) (8.0.4)
Requirement already satisfied: numpy<2.3.0,>=2 in c:\users\vinay\anaconda3\lib\sit
e-packages (from opencv-python) (2.2.6)
Requirement already satisfied: colorama in c:\users\vinay\anaconda3\lib\site-packa
ges (from click>=8.0->flask) (0.4.6)
Requirement already satisfied: MarkupSafe>=2.0 in c:\users\vinay\anaconda3\lib\sit
e-packages (from Jinja2>=3.0->flask) (2.1.1)
Note: you may need to restart the kernel to use updated packages.
Project structure created successfully
In [1]: %pip install flask opencv-python imutils
In [2]: import os
# Base project folder
BASE_DIR = "facial_auth_app"
# Create folders
os.makedirs(f"{BASE_DIR}/templates", exist_ok=True)
os.makedirs(f"{BASE_DIR}/auth_images", exist_ok=True)
# Create files
open(f"{BASE_DIR}/app.py", "w").close()
open(f"{BASE_DIR}/templates/index.html", "w").close()
print("Project structure created successfully")
In [3]: app_code = r'''
from flask import Flask, render_template, Response
import cv2
import os
import time
from datetime import datetime
app = Flask(__name__)
SAVE_DIR = "auth_images"
os.makedirs(SAVE_DIR, exist_ok=True)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)
mouth_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)
file:///E:/slash mark/WEBCAM.html 1/3
camera = cv2.VideoCapture(0)
camera_active = True
close_time = None
authenticated = False
def generate_frames():
    global authenticated, camera_active, close_time
    blink = False
    mouth = False
    while camera_active:
        success, frame = camera.read()
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
            mouths = mouth_cascade.detectMultiScale(roi_gray, 1.7, 20)
            if len(eyes) == 0:
                blink = True
            if len(mouths) > 0:
                mouth = True
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            # ---- LOGIN SUCCESS ---
            if blink and mouth and not authenticated:
                authenticated = True
                close_time = time.time() + 3   # close after 3 seconds
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                cv2.putText(frame, "LOGIN SUCCESS",
                            (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0,255,0), 2)
                cv2.imwrite(
                    os.path.join(SAVE_DIR, f"login_success_{timestamp}.png"),
                    frame
                )
        # ---- AUTO CLOSE CAMERA ---
        if authenticated and close_time and time.time() >= close_time:
            camera_active = False
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()
@app.route('/')
def index():
    return render_template("index.html")
file:///E:/slash mark/WEBCAM.html 2/3
app.py written successfully
index.html written successfully
^C
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(debug=True)
'''
with open("facial_auth_app/app.py", "w", encoding="utf-8") as f:
    f.write(app_code)
print("app.py written successfully")
In [4]: html_code = r'''
<!DOCTYPE html>
<html>
<head>
    <title>Task 4 – Web-Based Facial Authentication</title>
</head>
<body style="text-align:center; font-family:Arial">
    <h2>Task 4 – Web-Based Facial Authentication</h2>
    <p>Blink eyes and open mouth to authenticate</p>
    <img src="{{ url_for('video') }}" width="640" height="480">
</body>
</html>
'''
with open("facial_auth_app/templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)
print("index.html written successfully")
In [5]: !cd facial_auth_app && python app.py
In [ ]: 
file:///E:/slash mark/WEBCAM.html
