import pandas as pd
import json
from extract_db import get_user_comments

# Get the data
comments_df = get_user_comments()

# Generate alerts from the comments
def generate_alerts_from_df(df):
    output_rows = []

    for idx, row in df.iterrows():
        alerts = []
        content_preview = row["comment_text"][:100] + "..." if len(row["comment_text"]) > 100 else row["comment_text"]

        if row['sentiment_score'] < -0.1:
            alerts.append("⚠ Negative tone detected. It might be helpful to take a moment for a break.")
        if "removed" in row['comment_text'].lower() or "spam filter" in row['comment_text'].lower():
            alerts.append("🛑 Warning: This might be flagged or removed. Review for clarity and avoid controversial language.")
        if row['sentiment_score'] > 0.3:
            alerts.append("🌟 Positive vibes! This comment radiates good energy and encouragement.")
        if row['sentiment_score'] == 0.0 and row['upvotes'] <= 1:
            alerts.append("🧘 Neutral tone with low engagement. Try to be more specific or rephrase for better clarity.")
        if len(row['comment_text']) > 300:
            alerts.append("📚 This comment is very detailed! Consider breaking it up into shorter parts for better readability.")
        if row['upvotes'] == 0:
            alerts.append("🔍 Low engagement. Maybe encourage others to share their thoughts or expand the discussion.")
        if row['sentiment_score'] == 0.0:
            alerts.append("🤔 Neutral tone. Try adding more emotion or perspective to engage readers better.")
        if "financial" in row['comment_text'].lower():
            alerts.append("💡 Great financial advice! Keep sharing insights to help others manage their money effectively.")
        if "spam" in row['comment_text'].lower():
            alerts.append("🚫 Spam alert. Consider revising or avoiding repetitive links or phrases.")
        if not alerts:
            alerts.append("✅ No issues detected. Keep engaging positively!")

        output_rows.append({
            "Comment ID": row["id"],
            "Date": row["date"],
            "upvotes": row["upvotes"],
            "Content Preview": content_preview,
            "Alerts": " | ".join(alerts)
        })

    return pd.DataFrame(output_rows)

# Create the alert dataframe
alerts_df = generate_alerts_from_df(comments_df)

# Summarize the alerts
def summarize_alerts(alerts_df):
    total_comments = len(alerts_df)
    avg_sentiment = round(comments_df["sentiment_score"].mean(), 3)
    avg_upvotes = round(alerts_df["upvotes"].mean(), 2)

    if avg_sentiment > 0.2:
        overall_vibe = "🌞 Positive vibes dominate the discussion! Keep the good energy flowing!"
    elif avg_sentiment < -0.1:
        overall_vibe = "☁ There's a slightly negative tilt. Maybe drop some encouragement in the chat!"
    else:
        overall_vibe = "🧘 Balanced and neutral tone overall. A thoughtful bunch!"

    summary_message = f"""
🎯 Mission Report Complete! We've scanned the community insights, and here's the scoop:

💬 Total Comments Reviewed: {total_comments}
📊 Average Sentiment Score: {avg_sentiment}
👍 Average Upvotes per Comment: {avg_upvotes}

🌟 Overall Vibe:
{overall_vibe}

🚀 Next Move:
Keep encouraging engagement, shout out the contributors, and drop some thoughtful prompts to elevate the conversation even more!
"""
    return summary_message

# Save alerts to JSON
alerts_df.to_json("alerts.json", orient="records", indent=2)

# Save summary to TXT
summary_text = summarize_alerts(alerts_df)
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary_text)

print("✅ Alerts and summary exported!")

