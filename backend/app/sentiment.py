from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiments(comments, batch_size=16):
    sentiment_counts = {
        "positive": 0,
        "negative": 0
    }

    for i in range(0, len(comments), batch_size):
        batch = comments[i:i + batch_size]
        results = sentiment_pipeline(batch)

        for result in results:
            if result["label"] == "POSITIVE":
                sentiment_counts["positive"] += 1
            else:
                sentiment_counts["negative"] += 1

    sentiment_counts["neutral"] = 0  # placeholder

    return sentiment_counts