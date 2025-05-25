import os
from utils import get_env_var
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from summarise_feed import give_text

def generate_speech(text, voice_id,output_path="output/output1.mp3"):
    ELEVENLABS_API_KEY = get_env_var("ELEVENLABS_API_KEY")
    client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
    )        
    audio=client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2"
    )
    audio_bytes = b"".join(audio)

    play(audio_bytes)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)
def main():
    generate_speech(text=give_text(), voice_id="JBFqnCBsd6RMkjVDRZzb")
if __name__ == "__main__":
    main()