# 🎥 Real-Time YouTube Video Tracker

A full-stack real-time data engineering project using **Kafka**, **MongoDB**, and **Streamlit** to track and display YouTube video data by keyword.

---

## 🎓 Project Objective

> To build a real-time data pipeline that fetches YouTube videos using the YouTube Data API, streams them through Kafka, stores them in MongoDB, and visualizes the data using a Streamlit dashboard.

---

## 🧰 Tools & Technologies

- **Python 3.x**
- **Kafka** for real-time streaming
- **MongoDB** for NoSQL storage
- **Streamlit** for visualization
- **Docker Compose** for container orchestration

---

## ⚙️ Folder Structure

```
youtube_realtime_pipeline/
├── docker-compose.yml
├── producer/
│   └── producer.py
├── consumer/
│   └── consumer.py
├── streamlit/
│   └── dashboard.py
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-realtime-pipeline.git
cd youtube-realtime-pipeline
```

### 2. Add Your YouTube API Key

Edit `producer/producer.py` and replace:

```python
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
```

---

### 3. Docker Setup

#### ▶️ Create `docker-compose.yml`

Paste the following:

```yaml
services:

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  mongo-express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: admin
    depends_on:
      - mongo

volumes:
  mongo_data:
```

### 4. Start Docker Containers

```bash
docker compose up -d
```

Verify at: `http://localhost:8081` (Mongo Express)

---

## 🔧 Python Components

### 📢 5. Producer - `producer/producer.py`

Fetches videos using YouTube API and sends to Kafka.

```bash
pip install kafka-python requests
python producer/producer.py
```

### 🪑 6. Consumer - `consumer/consumer.py`

Reads messages from Kafka and stores in MongoDB.

```bash
pip install kafka-python pymongo
python consumer/consumer.py
```

### 🔺 7. Dashboard - `streamlit/dashboard.py`

Displays real-time video data from MongoDB.

```bash
pip install streamlit pymongo pandas
streamlit run streamlit/dashboard.py
```

---

## 🔄 Data Flow Summary

```
[ YouTube API ] → [ Kafka Producer ] → [ Kafka Topic ] → [ Kafka Consumer ] → [ MongoDB ] → [ Streamlit Dashboard ]
```

---

## ✅ Features

- Real-time video fetching by keyword
- Kafka message streaming
- MongoDB NoSQL storage
- Live Streamlit dashboard with:
  - Video table
  - Bar chart by channel
  - Top 5 videos

---

## 📚 Future Improvements

- Add filters by date/channel
- Schedule producer with Airflow
- Containerize all Python apps
- Add thumbnail previews

---

## 🧠 How to Use

1. Start Docker: `docker compose up -d`
2. Run `producer.py`: fetch YouTube videos
3. Run `consumer.py`: store in MongoDB
4. Launch dashboard: `streamlit run dashboard.py`

---

## © Author

Built by Rohan Suryawanshi\
For educational and portfolio purposes.

---

