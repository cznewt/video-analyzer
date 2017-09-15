#!/usr/bin/env python
from __future__ import print_function

import base64
import cv2
import json
import numpy as np
import os

import pyspark
from kafka import KafkaProducer
from pyspark import streaming
from pyspark.streaming import kafka

# USER PROVIDED PARAMS
ZK_QUORUM = '192.168.203.148:2181,192.168.25.219:2181,192.168.237.21:2181'
KAFKA_BROKERS = '192.168.25.220:9092'
IN_TOPIC_NAME = 'video-stream-in'
OUT_TOPIC_NAME = 'video-stream-out'
BATCH_DURATION = 30

# AUTO CONFIGURED PARAMS
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
CASCADE_PATH = os.path.join(BASE_PATH, 'cascades', 'haarcascade_frontalface_default.xml')
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)


def main():
    sc = pyspark.SparkContext("local[2]", appName="VideoAnalyzer")
    ssc = streaming.StreamingContext(sc, BATCH_DURATION)
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKERS,
        batch_size=512000,
        api_version=(0, 10, 1))

    video = kafka.KafkaUtils.createStream(ssc, ZK_QUORUM, "video-consumer", {IN_TOPIC_NAME: 1}).map(lambda x: json.loads(x[1]))

    def process(dataset):
        #print('HOVNO: %s' % datum['timestamp'])
        data = dataset.collect()
        for datum in data:
            try:
                jpg = base64.b64decode(datum.get('data', None))
            except TypeError:
                return
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
            datum['data'] = base64.b64encode(frame)
            producer.send(OUT_TOPIC_NAME,
                key=datum['camera_id'],
                value=json.dumps(datum))

    video.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()

