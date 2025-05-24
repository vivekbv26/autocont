import os
from utils import get_env_var
from elevenlabs.client import ElevenLabs
from elevenlabs import play

def generate_speech(text, voice_id,output_path="output/output.mp3"):
    ELEVENLABS_API_KEY = get_env_var("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = get_env_var("ELEVENLABS_VOICE_ID")

    client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
    )        
    audio=client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2"
    )
    play(audio)
    # response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb?output_format=mp3_44100_128")
    with open(output_path, "wb") as f:
        f.write(audio)
    return output_path
def main():
    generate_speech(text="Hello, Vicky how does this sound, I think it sounds pretty good", voice_id="JBFqnCBsd6RMkjVDRZzb")
if __name__ == "__main__":
    main()