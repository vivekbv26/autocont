import requests
import json
from utils import get_env_var
import time


def generate(input_path="output/output.mp3"):
    HEYGEN_API_KEY = get_env_var("HEYGEN_API_KEY")
    url = "https://upload.heygen.com/v1/asset"
    print(f"Using API key: {HEYGEN_API_KEY}")

    headers = {
        "Content-Type": "audio/mpeg",
        "X-Api-Key": HEYGEN_API_KEY,
    }

    file_path = input_path

    with open(file_path, "rb") as file:
        response = requests.post(url, headers=headers, data=file)
    print(response.status_code)
    generate_video(response.json().get("id"), title="Test Video", dimension="16:9")


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
        "caption": "This is a test video",
         "dimension": {
            "width": 1280,
            "height": 720
        },
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id":"Abigail_sitting_sofa_front",
                    "scale": 1.0,
                    "avatar_style": "normal",
                    "offset": {
                        "x": 0.0,
                        "y": 0.0
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
        print(f"Video request successful. Video ID: {result.get('video_id')}")
        return result
    else:
        print("Error creating video:", response.status_code, response.text)
        return None

def main():
    HEYGEN_API_KEY = get_env_var("HEYGEN_API_KEY")
    video_id = generate(input_path="output/output.mp3")

    if not video_id:
        print("Video ID not returned.")
        return

    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": HEYGEN_API_KEY
    }

    while True:
        response = requests.get(url, headers=headers)
        result = response.json()
        status = result.get("status")
        print("Video status:", status)

        if status == "completed":
            print("Video URL:", result.get("video_url"))
            break
        elif status == "failed":
            print("Video generation failed.")
            break

        time.sleep(5)

if __name__ == "__main__":
    main()