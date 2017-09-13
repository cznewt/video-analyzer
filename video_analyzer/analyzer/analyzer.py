import base64
import cv2
import json
import numpy as np
import os
import sys

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
CASCADE_PATH = os.path.join(BASE_PATH, 'cascades', 'haarcascade_frontalface_default.xml')
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)

while True:
    with open('payload.json', 'r') as fh:
        json_data = fh.read()

    data = json.loads(json_data)
    jpg = base64.b64decode(data.get('data', ''))
    frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

