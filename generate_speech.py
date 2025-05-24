import os
from utils import get_env_var
from elevenlabs.client import ElevenLabs
from elevenlabs import play

def generate_speech(text, voice_id,output_path="output/output.mp3"):
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
    generate_speech(text="Former President Donald Trump delivered a politically charged commencement address to the West Point Class of 2025, criticizing military diversity initiatives and touting his administration's defense policies. He emphasized the rollback of DEI programs and political training, highlighting his efforts to strengthen the military. Trump also announced a new $175 billion missile defense system aimed at countering threats from China and Russia, though experts warn it could trigger an arms race. Reuters A recent Pew Research study reveals that approximately 30% of Americans consult astrology, tarot cards, or fortune tellers at least once a year, with many viewing it as a form of entertainment rather than a serious practice. The study also notes that younger adults, particularly those aged 18 to 29, are more likely to engage in these practices. In San Antonio, a popular Mexican restaurant, which had been in business for over 60 years, has announced its closure. The decision comes as the city plans to construct a new development in the area, leading to the restaurant's closure despite its long-standing presence in the community. ", voice_id="JBFqnCBsd6RMkjVDRZzb")
if __name__ == "__main__":
    main()