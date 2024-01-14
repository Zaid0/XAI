import os
import pytube
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from elevenlabs import generate
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import pytube
from moviepy.editor import VideoFileClip, AudioFileClip
from elevenlabs import generate, play
# from tttt import transcript


def get_video_id(link):
    url_parts = urlparse(link)
    query = parse_qs(url_parts.query)
    video_id = query.get("v", [None])[0]
    return video_id

# def extract_audio(input_video_path, output_audio_path):
#     # Load the video clip
#     video_clip = VideoFileClip(input_video_path)
#
#     # Extract the audio
#     audio_clip = video_clip.audio
#
#     # Save the audio to a file
#     audio_clip.write_audiofile(output_audio_path, codec='mp3')
#
# def extract_instrumental(input_audio_path, output_instrumental_path):
#     separator = Separator('spleeter:2stems')
#
#     # Separate vocals and accompaniment
#     prediction = separator.separate_to_file(input_audio_path, output_instrumental_path)
#
#

def transcript(video_id='6zN1ocPd4Bs', language_code='ar', ):

    # Replace 'your_video_id' with the actual video ID
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])
    trans = ''

    for x in transcript.translate(language_code).fetch():
        trans+= '. ' + x['text']

    return trans




def dub_videos(audio_file_path, link, video_directory, video_filename, output_filename):
  video_id = get_video_id(link)
  audio_text = transcript(video_id)
  audio = generate(text=audio_text, voice="Daniel", model="eleven_multilingual_v2", api_key='8780696006e05ff0fa0eeebb58d8bd69')

  # Save the generated audio to a file
  with open(audio_file_path, "wb") as audio_file:
      audio_file.write(audio)

  # Download YouTube video
  yt = pytube.YouTube(link)
  stream = yt.streams.get_highest_resolution()

  # Specify the full file path including the filename
  video_file_path = os.path.join(video_directory, video_filename)

  # Ensure the directory exists, create if necessary
  os.makedirs(video_directory, exist_ok=True)

  # Download the video
  stream.download(filename=video_filename, output_path=video_directory)

  # Load the video clip
  video_clip = VideoFileClip(video_file_path)

  # Load the generated audio clip
  audio_clip = AudioFileClip(audio_file_path)

  # input_video_path = "video.mp4"
  # output_audio_path = "temp_audio.mp3"
  # output_instrumental_path = "instrumental"
  #
  # Extract audio from video
  # extract_audio(input_video_path, output_audio_path)

  # Extract instrumental using Spleeter
  # extract_instrumental(output_audio_path, output_instrumental_path)

  print('1111111111111111111111111111111111111111111111')

  # sound2 = AudioSegment.from_file('instrumental/temp_audio/accompaniment.wav', format='wav')
  # combined_clip = audio_clip.overlay(sound2)

  print('22222222222222222222222222222222222222222')

  # Combine video and audio
  video_with_audio = video_clip.set_audio(audio_clip)

  # Save the final video with audio
  output_file_path = os.path.join(video_directory, output_filename)
  video_with_audio.write_videofile(output_file_path, codec="libx264", audio_codec="aac")





# audio_file_path = "generated_audio.mp3"
# link = "https://www.youtube.com/watch?v=JC82Il2cjqA"
# video_id = 'JC82Il2cjqA'
# # Generate the audio
# video_directory = r"C:\Users\zaidr\$ML_PATH\dubbing"
# video_filename = "video.mp4"
# output_filename = "output_video.mp4"
# # print(transcript(video_id))
#
# if __name__ == "__main__":
#
#
#     dub_videos(audio_file_path, link, video_directory, video_filename, output_filename, video_id)
#
#
