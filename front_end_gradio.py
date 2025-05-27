import gradio as gr
from supabase import create_client, Client
from generate_speech import generate_speech
from summarise_feed import give_text
from utils import get_env_var
from add_audio import pipeline
from upload_video import upload_video
import random
import os
import time

def run_full_pipeline(voice_id, custom_text, video_number, upload_to_youtube, yt_title, yt_description, progress=gr.Progress()):
    logs = []
    try:
        progress(0.05, "Preparing text...")
        text = custom_text.strip() if custom_text.strip() else give_text()
        logs.append(f"Text used: {text[:80]}...")

        progress(0.2, "Generating speech...")
        audio_link = generate_speech(text=text, voice_id=voice_id)
        logs.append(f"Speech generated: {audio_link['signedURL']}")

        progress(0.4, f"Fetching video: output_{video_number}.mp4")
        url = get_env_var("SUPABASE_URL")
        key = get_env_var("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        video_url = supabase.storage.from_("background").get_public_url(f"output_{video_number}.mp4")
        logs.append(f"Video link: {video_url}")

        output_path = "output/output.mp4"
        progress(0.6, "Creating video...")
        pipeline(video_url, audio_link["signedURL"], output_video_path=output_path, font_path="font.ttf")
        logs.append("Final video created.")

        youtube_url = None
        if upload_to_youtube:
            progress(0.8, "Uploading to YouTube...")
            youtube_url = upload_video(
                file_path=output_path,
                title=yt_title,
                description=yt_description
            )
            logs.append("Video uploaded to YouTube.")
        else:
            logs.append("Upload skipped (checkbox unchecked).")

        progress(1.0, "Completed.")
        return "\n".join(logs), audio_link["signedURL"], output_path, youtube_url, output_path

    except Exception as e:
        return f"Error: {str(e)}", None, None, None, None


video_choices = list(range(1, 16))

with gr.Blocks(title="AI News Video Generator") as app:
    gr.Markdown("# AI News Video Generator\nGenerate short videos from text summaries, voices, and visuals.")

    with gr.Row():
        voice_input = gr.Textbox(label="Voice ID", value="JBFqnCBsd6RMkjVDRZzb")
        video_select = gr.Dropdown(choices=video_choices, label="Video Number", value=1)

    custom_textbox = gr.Textbox(label="Custom Text (Optional)", lines=4)

    with gr.Row():
        upload_toggle = gr.Checkbox(label="Upload to YouTube", value=True)
        yt_title_input = gr.Textbox(label="YouTube Title", value="You won't believe what just happened!")
        yt_desc_input = gr.Textbox(label="YouTube Description", value="Stay updated with the latest news in just 30 seconds!")

    generate_btn = gr.Button("Generate Video")

    logs_output = gr.Textbox(label="Logs", lines=10)
    audio_preview = gr.Audio(label="Generated Audio", interactive=False)
    video_preview = gr.Video(label="Final Video", interactive=False)
    youtube_link_output = gr.Textbox(label="YouTube Video URL", interactive=False)
    download_output = gr.File(label="Download Final Video")

    generate_btn.click(
        fn=run_full_pipeline,
        inputs=[
            voice_input,
            custom_textbox,
            video_select,
            upload_toggle,
            yt_title_input,
            yt_desc_input
        ],
        outputs=[
            logs_output,
            audio_preview,
            video_preview,
            youtube_link_output,
            download_output
        ]
    )

if __name__ == "__main__":
    app.launch()
