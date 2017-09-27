from kafka import KafkaConsumer
from kafka import TopicPartition

KAFKA_BROKERS = 'kafka-video-stream-2-0:9092'
OUT_TOPIC_NAME = 'video-stream-out'

consumer = KafkaConsumer(OUT_TOPIC_NAME, bootstrap_servers=KAFKA_BROKERS, api_version=(0, 10, 1))

print consumer.topics()
print consumer.subscription()
print consumer.partitions_for_topic(OUT_TOPIC_NAME)
print consumer.assignment()

for msg in consumer.poll():
    print (msg)

