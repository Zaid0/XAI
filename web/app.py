from dd import dub_videos
import streamlit as st

# Streamlit app layout
st.title("Video Processing App")

# Text input for URL
url = st.text_input("Enter the URL of the video:")
audio_file_path = "generated_audio.mp3"
link = "https://www.youtube.com/watch?v=JC82Il2cjqA"
video_id = 'JC82Il2cjqA'
# Generate the audio
video_directory = r"C:\Users\zaidr\$ML_PATH\dubbing"
video_filename = "video.mp4"
output_filename = "output_video.mp4"


if url:
    video_path = r'C:\Users\zaidr\$ML_PATH\dubbing\output_video.mp4'
    dub_videos(audio_file_path, url, video_directory, video_filename, output_filename, )
    # Display the processed video (optional)
    st.video(video_path)

    # Provide a download link for the video
    with open(video_path, "rb") as file:
        btn = st.download_button(
            label="Download Video",
            data=file,
            file_name="processed_video.mp4",
            mime="video/mp4"
        )



