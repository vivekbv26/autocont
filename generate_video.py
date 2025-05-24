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
            "width": 1280,
            "height": 720
        },
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id":"Conrad_sitting_sofa_front",
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
        print(result)
        print(f"Video request successful. Video ID: {result.get('data')['video_id']}")
        return (result.get('data')['video_id'])
    else:
        print("Error creating video:", response.status_code, response.text)
        return None

def main():
    HEYGEN_API_KEY = get_env_var("HEYGEN_API_KEY")
    video_id = generate(input_path="output/output.mp3")
    print("Video ID:", video_id)
    if not video_id:
        print("Video ID not returned.")
        return

    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": HEYGEN_API_KEY
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    status = result.get("data")['status']
    while (status != "completed" and status != "failed"):
        response = requests.get(url, headers=headers)
        result = response.json()

        status = result.get("data")["status"]
        print("Current status:", status)
        if status == "completed":
            print("Video URL:", result.get("data")['video_url'])
            break
        elif status == "failed":
            print("Video generation failed.")
            break

        time.sleep(5)

if __name__ == "__main__":
    main()