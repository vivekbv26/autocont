from supabase import create_client, Client
from generate_speech import generate_speech
from summarise_feed import give_text
from utils import get_env_var
import random
from add_audio import pipeline



print("Generating speech...")
audio_link=generate_speech(text=give_text(), voice_id="JBFqnCBsd6RMkjVDRZzb")
print("Speech generated successfully.")
print(audio_link["signedURL"])
url=get_env_var("SUPABASE_URL")
key=get_env_var("SUPABASE_KEY")
supabase: Client = create_client(url, key)
random_number = random.randint(1, 15)
video_link = (
    supabase.storage
    .from_("background")
    .get_public_url(
    f"output_{random_number}.mp4", 
    ))
print(video_link)
pipeline(video_link,audio_link["signedURL"], output_video_path="output.mp4", font_path="font.ttf")