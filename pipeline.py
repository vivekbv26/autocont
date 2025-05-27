from supabase import create_client, Client
from generate_speech import generate_speech
from summarise_feed import give_text
from utils import get_env_var
import random
from add_audio import pipeline
from upload_video import upload_video

def execute(text=give_text(), 
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            font_path="fonts/font.ttf",
            title="You won't believe what just happened!",
            description="Stay updated with the latest news in just 30 seconds!"):
    print("Generating speech...")

        # N2lVS1w4EtoT3dr4eOWO

        # ThT5KcBeYPX3keUQqHPh dorothy
    audio_link=generate_speech(text, voice_id)
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

    pipeline(video_link,audio_link["signedURL"], output_video_path="output/output.mp4", font_path=font_path)
    supabase.storage.from_("audio").upload(file="output/output.mp4", path="testdeploy.mp3",file_options={
            "content-type": "video/mp4",
            "cache-control": "3600",
            "upsert": "true"
        })
    upload_video(
        file_path="output/output.mp4",
        title=title,
        description=description,
    )
execute()