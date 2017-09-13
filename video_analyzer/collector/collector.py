import base64
import cv2
import json
import time
import urllib 
import numpy as np

CAMERA_ID = 'cam-01'
STREAM_URL = 'http://cfg.newt.cz:8888/?action=stream'


stream = urllib.urlopen(STREAM_URL)
bytes = ''
while True:
    bytes += stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        payload = {
          'camera_id': CAMERA_ID,
          'timestamp': int(time.time()),
          'rows': frame.shape[0],
          'cols': frame.shape[1],
          'type': 'uint8',
          'data': base64.b64encode(jpg)
        }

        with open('payload.json', 'w') as fh:
            json.dump(payload, fh)

        break
