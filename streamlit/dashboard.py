import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["youtube"]
collection = db["videos"]

# Fetch data from MongoDB
def fetch_video_data():
    videos = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(videos)

# Streamlit UI
st.set_page_config(page_title="📺 YouTube Video Tracker", layout="wide")
st.title("📊 Real-Time YouTube Video Tracker")

df = fetch_video_data()

if df.empty:
    st.warning("No data found in MongoDB.")
else:
    st.dataframe(df.sort_values("published_at", ascending=False), use_container_width=True)
    st.bar_chart(df['channel'].value_counts())

    st.subheader("Top Videos")
    for _, row in df.head(5).iterrows():
        st.markdown(f"- **{row['title']}** by *{row['channel']}*")

