import json
import time
import requests
from kafka import KafkaProducer

# Replace with your own YouTube API Key
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
SEARCH_QUERY = 'python programming'
KAFKA_TOPIC = 'youtube_videos'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_youtube_videos():
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={SEARCH_QUERY}&key={YOUTUBE_API_KEY}&maxResults=5"
    response = requests.get(url)
    data = response.json()

    if 'items' not in data:
        print("Error: No video data found.")
        print(data)
        return []

    videos = []
    for item in data['items']:
        video = {
            'video_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'published_at': item['snippet']['publishedAt']
        }
        videos.append(video)

    return videos

def send_to_kafka(videos):
    for video in videos:
        print(f"Sending video to Kafka: {video['title']}")
        producer.send(KAFKA_TOPIC, value=video)
    producer.flush()

if __name__ == '__main__':
    while True:
        print("Fetching latest YouTube videos...")
        video_list = fetch_youtube_videos()
        if video_list:
            send_to_kafka(video_list)
        time.sleep(60)  # fetch every 60 seconds
