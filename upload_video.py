import os
import json
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils import get_env_var
# Load secrets from environment variables
CLIENT_ID = get_env_var("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = get_env_var("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = get_env_var("YOUTUBE_REFRESH_TOKEN")

# File path of the video
VIDEO_FILE = "output/output.mp4"

def get_credentials():
    creds_data = {
        "token": "",
        "refresh_token": REFRESH_TOKEN,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scopes": ["https://www.googleapis.com/auth/youtube.upload"]
    }

    creds = Credentials.from_authorized_user_info(info=creds_data)
    if not creds.valid or creds.expired:
        request = Request()
        creds.refresh(request)
    return creds

def upload_video(file_path, title, description, tags=None):
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["cybercrime", "conspiracy", "unsolved mystery", "cult",
    "espionage", "paranormal", "forbidden", "secret society", "ritual",
    "black market", "scandal", "hidden truth", "classified", "covert operation",
    "did you know", "bizarre", "unbelievable", "shocking", "unexplained"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(file_path, resumable=True)
    upload_request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = upload_request.execute()
    print(f"[✅] Video uploaded successfully: https://youtube.com/watch?v={response['id']}")

