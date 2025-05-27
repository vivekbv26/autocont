import requests
import os

# Your provided API Key from Pexels
PEXELS_API_KEY = 'AVmiT6zUC6WMvPb9E23EyCv5pUUAdM8qo7lgOd0KF0947sKIfOCV2opw'

# Configuration
SEARCH_QUERY = 'sky diving vidoe'
NUM_VIDEOS = 2 # You can adjust this number as needed
DOWNLOAD_FOLDER = 'gameplay_videos'

# Create the download folder
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# API request headers and parameters
headers = {
    'Authorization': PEXELS_API_KEY,
}

params = {
    'query': SEARCH_QUERY,
    'per_page': NUM_VIDEOS,
}

# Make the API call to Pexels
response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)

# Check if request was successful
if response.status_code == 200:
    videos = response.json()['videos']
    for i, video in enumerate(videos):
        # Select the highest resolution available
        video_file = max(video['video_files'], key=lambda x: x['height'])
        video_url = video_file['link']

        print(f'Downloading video {i+1} from: {video_url}')

        # Download video data
        video_data = requests.get(video_url).content
        file_path = os.path.join(DOWNLOAD_FOLDER, f'gameplay_video_{i+1}.mp4')

        # Save the video to local disk
        with open(file_path, 'wb') as f:
            f.write(video_data)

        print(f'Video {i+1} downloaded successfully to {file_path}')
else:
    print(f' Failed to retrieve videos. Status code: {response.status_code}, Reason: {response.text}')
