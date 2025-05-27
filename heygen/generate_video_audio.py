import requests
import json
from utils import get_env_var
import time


def generate(input_path="output/output1.mp3"):
    HEYGEN_API_KEY = get_env_var("HEYGEN_API_KEY")
    url = "https://upload.heygen.com/v1/asset"

    headers = {
        "Content-Type": "audio/mpeg",
        "X-Api-Key": HEYGEN_API_KEY,
    }

    file_path = input_path

    with open(file_path, "rb") as file:
        response = requests.post(url, headers=headers, data=file)
    print(response.status_code)
    print(response.json().get("data")['id'])
    return generate_video(response.json().get("data")['id'], title="Test Video", dimension="16:9")


def generate_video(audio_asset_id,title="try",dimension="16:9"):
    HEYGEN_API_KEY = get_env_var("HEYGEN_API_KEY")
    url = "https://api.heygen.com/v2/video/generate"
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": HEYGEN_API_KEY
    }
    payload = {
        "title": title,
        "caption": False,
         "dimension": {
            "width": 720,
            "height": 1080
        },
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id":"7890302cd10645e1900cea865a8268fb",
                    "scale": 1.0,
                    "avatar_style": "normal",
                    "offset": {
                        "x": 0.0,
                        "y": 0.3,
                    }
                },
                "voice": {
                    "type": "audio",
                    "audio_asset_id": audio_asset_id
                },
                "background": {
                    "type": "color",
                    "value": "#f6f6fc"
                }
            }
        ]
    }
    response=requests.post(url,headers=headers,data=json.dumps(payload))
    if response.status_code==200:
        result = response.json()
        print(result)
        print(f"Video request successful. Video ID: {result.get('data')['video_id']}")
        return (result.get('data')['video_id'])
    else:
        print("Error creating video:", response.status_code, response.text)
        return None
