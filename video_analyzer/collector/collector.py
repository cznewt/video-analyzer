import base64
import cv2
import json
import time
import urllib 
import numpy as np
import sys

from kafka import KafkaProducer

# USER PROVIDED PARAMS 
CAMERA_ID = 'cam-01'
STREAM_URL = 'http://cfg.newt.cz:8888/?action=stream'
KAFKA_BROKERS = 'kafka-video-kafka-0.kafka-video-kafka.default.svc.atengler-deploy-heat-k8s-ha-calico-173.bud-mk.local:9092'
IN_TOPIC_NAME = 'video-stream-in'


try:
    stream = urllib.urlopen(STREAM_URL)
except Exception as e:
    print "%s ERROR [%s] Connecting to video stream failed with following reason: %s" % (
        time.strftime('%y/%m/%d %H:%M:%S'), CAMERA_ID, repr(e))
    sys.exit(1)

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

        print "%s INFO [%s] Frame sent" % (time.strftime('%y/%m/%d %H:%M:%S'), CAMERA_ID)

        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKERS,
                batch_size=512000,
                api_version=(0, 10, 1))
        except Exception as e:
            print "%s ERROR [%s] Connecting to Kafka broker failed with following reason: %s" % (
                time.strftime('%y/%m/%d %H:%M:%S'), CAMERA_ID, repr(e))
        try:
            producer.send(IN_TOPIC_NAME,
                key=CAMERA_ID,
                value=json.dumps(payload))
            print "%s INFO [%s] Frame sent" % (time.strftime('%y/%m/%d %H:%M:%S'), CAMERA_ID)
        except Exception as e:
            print "%s ERROR [%s] Sending frame failed with following error: %s" % (
                time.strftime('%y/%m/%d %H:%M:%S'), CAMERA_ID, repr(e))

