from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import asyncio
import pytube
from moviepy.editor import VideoFileClip, AudioFileClip
from elevenlabs import generate
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()


class DubVideosRequest(BaseModel):
    audio_file_path: str
    link: str
    video_id: str
    video_directory: str
    video_filename: str
    output_filename: str


async def transcript(video_id, language_code='ar'):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])
    trans = ''

    for x in transcript.translate(language_code).fetch():
        trans += '. ' + x['text']

    return trans


async def generate_audio(audio_text, audio_file_path):
    audio = generate(text=audio_text, voice="Daniel", model="eleven_multilingual_v2",
                     api_key='8780696006e05ff0fa0eeebb58d8bd69', latency=5)
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio)


async def download_video(link, video_directory, video_filename):
    yt = pytube.YouTube(link)
    stream = yt.streams.get_highest_resolution()
    return await asyncio.to_thread(stream.download, filename=video_filename, output_path=video_directory)


async def process_video(video_file_path, audio_file_path, output_file_path):
    try:
        video_clip = VideoFileClip(video_file_path)
        audio_clip = AudioFileClip(audio_file_path)
        video_with_audio = video_clip.set_audio(audio_clip)
        await asyncio.to_thread(video_with_audio.write_videofile, output_file_path, codec="libx264", audio_codec="aac")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dub_videos/")
async def dub_videos_api(request: DubVideosRequest):
    try:
        audio_text = await transcript(request.video_id)
        await generate_audio(audio_text, request.audio_file_path)

        video_file_path = os.path.join(request.video_directory, request.video_filename)
        output_file_path = os.path.join(request.video_directory, request.output_filename)
        os.makedirs(request.video_directory, exist_ok=True)

        # Ensure video is downloaded before processing
        await download_video(request.link, request.video_directory, request.video_filename)
        await process_video(video_file_path, request.audio_file_path, output_file_path)

        return {"message": "Video processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "_main_":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)