import requests
import json
from utils import get_env_var
import time
from generate_video_audio import generate
from generate_video_text import generate_video_text
from summarise_feed import give_text

def main():
    HEYGEN_API_KEY = get_env_var("HEYGEN_API_KEY")
    a=0
    text = give_text()
    print(text)
    if(a==1):
        video_id = generate(input_path="output/output1.mp3")
    else:
        video_id = generate_video_text(text=text, title="try")
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