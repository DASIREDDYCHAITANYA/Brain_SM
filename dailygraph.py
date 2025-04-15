# generate_sentiment_data.py
import praw
import json
from textblob import TextBlob
from datetime import datetime, timedelta, timezone

print("✅ Script started!")
print("⏳ Fetching comments...")

reddit = praw.Reddit(
    client_id='xTs9ILMTPdG414PC6pek2w',
    client_secret='GhATf7qAYfWjG7wTjTlngkU-Fb_k-w',
    user_agent='BrainFunctionScript/1.0 by Chaitanya'
)

def fetch_recent_comments(username='The_Adventurer_73', limit=100):
    user = reddit.redditor(username)
    now = datetime.now(timezone.utc)
    past_24h = now - timedelta(hours=24)

    data = []
    for comment in user.comments.new(limit=limit):
        comment_time = datetime.fromtimestamp(comment.created_utc, timezone.utc)
        if comment_time >= past_24h:
            score = TextBlob(comment.body).sentiment.polarity
            data.append({
                "comment": comment.body,
                "created_utc": comment_time.isoformat(),
                "sentiment_score": score
            })

    with open("sentiment_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Data saved to sentiment_data.json")
    print(f"📊 Total comments fetched in 24h: {len(data)}")

fetch_recent_comments()