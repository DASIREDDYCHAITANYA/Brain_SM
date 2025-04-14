from textblob import TextBlob
import praw
import pandas as pd
from datetime import datetime

# Initialize Reddit API
reddit = praw.Reddit(
    client_id='xTs9ILMTPdG414PC6pek2w',
    client_secret='GhATf7qAYfWjG7wTjTlngkU-Fb_k-w',
    user_agent='BrainFunctionScript/1.0 by Chaitanya'
)

def get_user_comments(username='dequeued',limit=20):

    user = reddit.redditor(username)

    comment_data = []
    for comment in user.comments.new(limit=limit):
        try:
            date = datetime.fromtimestamp(comment.created_utc).strftime('2025-04-02')
            text = comment.body
            sentiment_score = TextBlob(text).sentiment.polarity
            upvotes = comment.ups
            num_replies = len(list(comment.replies))  # Optional info

            comment_data.append({
                'id': comment.id,
                'date': date,
                'upvotes': upvotes,
                'comment_text': text,
                'sentiment_score': sentiment_score
            })
        except Exception as e:
            print(f"Error processing comment {comment.id}: {e}")

    df = pd.DataFrame(comment_data)
    v=df.head(20)
    return v

