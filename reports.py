import praw
import pandas as pd
from textblob import TextBlob
from datetime import datetime, timedelta

# Initialize Reddit API
reddit = praw.Reddit(
    client_id='xTs9ILMTPdG414PC6pek2w',
    client_secret='GhATf7qAYfWjG7wTjTlngkU-Fb_k-w',
    user_agent='BrainFunctionScript/1.0 by Chaitanya'
)

def fetch_user_comments(username='The_Adventurer_73', limit=100):
    now = datetime.utcnow()
    past_24h = now - timedelta(hours=24)
    comment_data = []

    user = reddit.redditor(username)

    for comment in user.comments.new(limit=limit):
        comment_time = datetime.utcfromtimestamp(comment.created_utc)
        if comment_time >= past_24h:
            sentiment = TextBlob(comment.body).sentiment.polarity
            comment_data.append({
                'timestamp': comment_time.strftime('%Y-%m-%d %H:%M:%S'),
                'text': comment.body,
                'sentiment': round(sentiment, 3),
                'upvotes': comment.ups
            })
    return comment_data

def generate_html_report(username='The_Adventurer_73'):
    comments = fetch_user_comments(username)
    if not comments:
        html = """
        <html>
        <head><title>No Comments</title></head>
        <body><h2>No comments found in the past 24 hours.</h2></body>
        </html>
        """
    else:
        df = pd.DataFrame(comments)
        avg_sentiment = df['sentiment'].mean()
        avg_upvotes = df['upvotes'].mean()
        most_pos = df.loc[df['sentiment'].idxmax()]
        most_neg = df.loc[df['sentiment'].idxmin()]

        # Contextual summary
        if avg_sentiment > 0.5:
            sentiment_summary = "The user exhibits a highly positive tone overall, suggesting optimistic and supportive engagement."
        elif avg_sentiment > 0:
            sentiment_summary = "The user generally maintains a positive outlook, with occasional neutral or mixed expressions."
        elif avg_sentiment == 0:
            sentiment_summary = "The user's sentiment is neutral overall, possibly indicating balanced or factual communication."
        elif avg_sentiment > -0.5:
            sentiment_summary = "The user tends to lean toward slightly negative sentiment, which could reflect criticism or concern."
        else:
            sentiment_summary = "The user shows a strong negative sentiment, possibly signaling dissatisfaction, frustration, or distress."

        html = f"""
        <html>
        <head>
            <title>Sentiment Report for {username}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background: linear-gradient(to right, #e3f2fd, #ffffff);
                    padding: 20px;
                    animation: fadeIn 1s ease-in-out;
                }}
                h2 {{ color: #0d47a1; }}
                .summary {{
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    animation: slideUp 0.8s ease-out;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                    background: white;
                    animation: fadeIn 1.2s ease-in;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #1976d2;
                    color: white;
                }}
                tr:hover {{ background-color: #f1f1f1; }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                @keyframes slideUp {{
                    from {{ transform: translateY(20px); opacity: 0; }}
                    to {{ transform: translateY(0); opacity: 1; }}
                }}
            </style>
        </head>
        <body>
            <h2>Sentiment Analysis Report for u/{username}</h2>
            <div class="summary">
                <p><strong>Total Comments:</strong> {len(df)}</p>
                <p><strong>Average Sentiment Score:</strong> {avg_sentiment:.3f}</p>
                <p><strong>Average Upvotes:</strong> {avg_upvotes:.2f}</p>
                <p><strong>Most Positive Comment:</strong> {most_pos['text']}</p>
                <p><strong>Most Negative Comment:</strong> {most_neg['text']}</p>
            </div>

            <h3>All Comments</h3>
            <table>
                <tr><th>Timestamp</th><th>Comment</th><th>Sentiment</th><th>Upvotes</th></tr>
        """

        for _, row in df.iterrows():
            html += f"<tr><td>{row['timestamp']}</td><td>{row['text']}</td><td>{row['sentiment']}</td><td>{row['upvotes']}</td></tr>"

        html += f"""
            </table>
            <div class="summary" style="margin-top: 30px;">
                <h3>Contextual Summary</h3>
                <p>{sentiment_summary}</p>
            </div>
        </body>
        </html>
        """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Animated HTML report saved to sentiment_report.html")

# Run it
generate_html_report()