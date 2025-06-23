# services/uploadVideo.py

import datetime
from fastapi import HTTPException
from pydantic import BaseModel, validator
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
import os
import pickle
import time

# Schema dữ liệu
class VideoUpload(BaseModel):
    video_url: str
    title: str
    description: str
    category: str = "22"
    privacy: str = "private"

    @validator("video_url", "title", "description")
    def not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v

# Cấu hình YouTube API
CLIENT_SECRET_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/yt-analytics.readonly"]

def get_credentials():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds

def get_youtube_service():
    creds = get_credentials()
    return build("youtube", "v3", credentials=creds)

def get_analytics_service():
    creds = get_credentials()
    return build("youtubeAnalytics", "v2", credentials=creds)

def get_channel_id(youtube):
    response = youtube.channels().list(
        part="id",
        mine=True
    ).execute()
    return response["items"][0]["id"]

def download_video(video_url: str, output_path: str):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return output_path
    else:
        raise Exception(f"Failed to download video from URL. Status code: {response.status_code}")

def handle_upload(video_data: VideoUpload):
    video_path = "temp_video.mp4"
    try:
        # Tải video
        download_video(video_data.video_url, video_path)

        # Xác thực
        youtube = get_youtube_service()

        # Metadata
        body = {
            "snippet": {
                "title": video_data.title,
                "description": video_data.description,
                "tags": ["video", "upload"],
                "categoryId": video_data.category,
            },
            "status": {
                "privacyStatus": video_data.privacy,
            },
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if response is not None:
                media.stream().close()
                return {"message": "Video uploaded successfully", "video_id": response["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(video_path):
            try:
                time.sleep(1)
                os.remove(video_path)
            except PermissionError:
                pass

def get_video_stats(video_id: str):
    try:
        youtube = get_youtube_service()

        response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        items = response.get("items", [])
        if not items:
            raise HTTPException(status_code=404, detail="Video not found")

        stats = items[0]["statistics"]
        return {
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video stats error: {str(e)}")