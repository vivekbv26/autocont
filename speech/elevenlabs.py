from utils import get_env_var
from elevenlabs.client import ElevenLabs
from elevenlabs import play

def use_elevenslabs(text,voice_id):
    ELEVENLABS_API_KEY = get_env_var("ELEVENLABS_API_KEY")
    client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
    )        
    audio=client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_turbo_v2_5"
    )
    audio_bytes = b"".join(audio)
    return audio_bytes