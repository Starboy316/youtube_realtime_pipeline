from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Kafka config
KAFKA_TOPIC = 'youtube_videos'
KAFKA_BROKER = 'localhost:9092'

# MongoDB config
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'youtube'
MONGO_COLLECTION = 'videos'

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
video_collection = mongo_db[MONGO_COLLECTION]

# Connect to Kafka
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='youtube-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🎧 Listening to Kafka...")

for message in consumer:
    video_data = message.value
    print(f"📥 Saving to MongoDB: {video_data['title']}")
    
    # Avoid duplicates (upsert)
    video_collection.update_one(
        {'video_id': video_data['video_id']},
        {'$set': video_data},
        upsert=True
    )
