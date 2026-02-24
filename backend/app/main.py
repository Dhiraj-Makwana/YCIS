from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from app.youtube import fetch_comments
from app.sentiment import analyze_sentiments
from app.database import save_comments

app = FastAPI(title="YouTube Comment Intelligence System")

class VideoRequest(BaseModel):
    video_url: HttpUrl
    max_comments: int = 200


@app.post("/analyze")
def analyze_video(data: VideoRequest):
    try:
        # Fetch comments
        comments = fetch_comments(data.video_url, max_comments=data.max_comments)

        if not comments:
            raise HTTPException(status_code=404, detail="No comments found for this video.")

        # Store comments in MongoDB
        save_comments(comments)

        # Run sentiment analysis
        sentiment_result = analyze_sentiments(comments)

        return {
            "status": "success",
            "total_comments": len(comments),
            "sentiment_distribution": sentiment_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))