from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from app.youtube import fetch_comments
from app.sentiment import analyze_sentiments
from app.database import save_comments
from app.toxicity import detect_toxicity
from app.embeddings import generate_embeddings
from app.clustering import cluster_comments

app = FastAPI(title="YouTube Comment Intelligence System")

class VideoRequest(BaseModel):
    video_url: HttpUrl
    max_comments: int = 200


@app.post("/analyze")
def analyze_video(data: VideoRequest):

    print("Starting analysis...")

    try:

        # Convert HttpUrl to string
        video_url = str(data.video_url)

        # Fetch comments
        comments = fetch_comments(video_url, max_comments=data.max_comments)
        print("Comments fetched:", len(comments))

        if not comments:
            raise HTTPException(status_code=404, detail="No comments found for this video.")
        
        # Store comments in MongoDB
        save_comments(comments)
        print("Comments saved to MongoDB")

        #sentiment analysis
        sentiment_result = analyze_sentiments(comments)
        print("Sentiment analysis done")

        #Toxicity detection
        toxicity_result = detect_toxicity(comments)
        print("Toxicity analysis done")

        # Generate embeddings
        embeddings = generate_embeddings(comments)
        print("Embeddings generated")

        # Cluster comments
        clusters = cluster_comments(comments, embeddings)
        print("clusters generated")

        return {
            "status": "success",
            "total_comments": len(comments),
            "sentiment_distribution": sentiment_result,
            "toxicity_analysis": toxicity_result,
            "embedding_dimension": len(embeddings[0]),
            "comment_clusters": clusters
        }

    except Exception as e:
        print("ERROR OCCURRED:", e)
        raise HTTPException(status_code=500, detail=str(e))