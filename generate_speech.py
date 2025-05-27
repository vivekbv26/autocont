import os
from utils import get_env_var
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from summarise_feed import give_text
from supabase import create_client, Client
from speech.elevenlabs import use_elevenslabs
from speech.polly import use_polly

def generate_speech(text, voice_id,output_path="output/output1.mp3"):
    url=get_env_var("SUPABASE_URL")
    key=get_env_var("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    audio_bytes = use_polly(text)
    supabase.storage.from_("audio").upload(file=audio_bytes, path="output.mp3",file_options={
            "content-type": "audio/mpeg",
            "cache-control": "3600",
            "upsert": "true"
        })
    response = (
    supabase.storage
    .from_("audio")
    .create_signed_url(
        "output.mp3", 
        600
    )
)
    return response
