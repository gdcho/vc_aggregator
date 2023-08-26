import openai
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
from io import BytesIO
from googleapiclient.discovery import build
from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
import urllib.request
import ssl
from pytube import YouTube
from moviepy.editor import VideoFileClip as EditorVideoFileClip
ssl._create_default_https_context = ssl._create_unverified_context

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

output_folder = "//Users/davidcho/vc_aggregator/output_folder"

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
pexels_api_key = os.getenv("PEXELS_API_KEY")
openai.api_key = api_key
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=youtube_api_key)


def generate_fact_prompt():
    return "Give me around 75 words based on an interesting fact."


def generate_subject_noun_prompt(fact):
    return f"Based on the generated fact, {fact}, return a main subject noun."


def fetch_pexels_videos(keyword):
    pexels_url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=3"
    headers = {"Authorization": pexels_api_key}
    response = requests.get(pexels_url, headers=headers, timeout=30)
    pexels_data = response.json()
    return pexels_data.get('videos', [])


fact_prompt = generate_fact_prompt()
fact_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=fact_prompt,
    max_tokens=200,
    stop=None
)
generated_fact = fact_response.choices[0].text.strip()

noun_prompt = generate_subject_noun_prompt(generated_fact)
noun_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=noun_prompt,
    max_tokens=30,
    stop=None
)
generated_noun = noun_response.choices[0].text.strip()

# Fetch Pexels
videos = fetch_pexels_videos(generated_noun)

print(f"\nGenerated Fact: {generated_fact}")
print(f"\nGenerated Noun: {generated_noun}\n")
if videos:
    for video in videos:
        print(f"Pexel URL: {video['url']}")
else:
    print("No videos found.")

# Fetch YouTube
search_query = generated_noun + " free stock footage"
request = youtube.search().list(q=search_query, part='snippet', maxResults=3)
response = request.execute()
print("\nYouTube:")
if 'items' in response:
    for video_info in response['items']:
        video_id = video_info['id'].get('videoId')
        if video_id:
            print(
                f"YouTube Video Link: https://www.youtube.com/watch?v={video_id}")
        else:
            print("No 'videoId' found for this item.")
else:
    print("No videos found.")

# gTTS - Text to Speech
tts = gTTS(generated_fact, lang='en', tld='com.au', slow=False)
audio_bytes = BytesIO()
tts.write_to_fp(audio_bytes)
audio_bytes.seek(0)

temp_audio_filename = "temp_audio.mp3"
with open(temp_audio_filename, "wb") as f:
    f.write(audio_bytes.read())

tts_audio_clip = AudioFileClip(temp_audio_filename)
os.remove(temp_audio_filename)

# Fetch Pexels
pexels_videos = fetch_pexels_videos(generated_noun)
pexels_video_clips = []

for video_info in pexels_videos:
    video_files = video_info.get('video_files', [])

    if video_files:
        video_url = next(
            (file['link'] for file in video_files if file['file_type'] == 'video/mp4'), None)

        if video_url:
            video_filename = os.path.basename(
                urllib.parse.urlparse(video_url).path)
            video_filename = os.path.join(output_folder, video_filename)
            urllib.request.urlretrieve(video_url, video_filename)
            pexels_video_clip = VideoFileClip(video_filename)
            pexels_video_clip = pexels_video_clip.subclip(
                0, tts_audio_clip.duration//3).set_duration(tts_audio_clip.duration//3)
            pexels_video_clips.append(pexels_video_clip)

# Fetch YouTube
youtube_video_clips = []

for video_info in response.get('items', []):
    video_id = video_info.get('id', {}).get('videoId')

    if video_id:
        youtube_video_url = f"https://www.youtube.com/watch?v={video_id}"

        yt = YouTube(youtube_video_url)
        video_stream = yt.streams.filter(
            progressive=True, file_extension="mp4").order_by("resolution").desc().first()

        video_filename = os.path.join(
            output_folder, f"youtube_video_{video_id}.mp4")

        video_stream.download(output_path=output_folder,
                              filename=os.path.basename(video_filename))

        youtube_video_clip = VideoFileClip(video_filename)
        youtube_video_clip = youtube_video_clip.subclip(
            0, tts_audio_clip.duration//3).set_duration(tts_audio_clip.duration//3)
        youtube_video_clips.append(youtube_video_clip)

for pexels_clip in pexels_video_clips:
    pexels_clip = pexels_clip.set_duration(tts_audio_clip.duration//3)

for youtube_clip in youtube_video_clips:
    youtube_clip = youtube_clip.set_duration(tts_audio_clip.duration//3)

video_width = 1080
video_height = 1920

stacked_pexels_videos = concatenate_videoclips(
    pexels_video_clips, method="compose")
stacked_pexels_videos = stacked_pexels_videos.resize(
    (video_width, video_height))

stacked_youtube_videos = concatenate_videoclips(
    youtube_video_clips, method="compose")
stacked_youtube_videos = stacked_youtube_videos.resize(
    (video_width, video_height))


final_video = CompositeVideoClip(
    [stacked_pexels_videos, stacked_youtube_videos], size=(video_width, video_height))

final_video_duration = min(tts_audio_clip.duration, final_video.duration)
final_video = final_video.set_audio(tts_audio_clip.subclip(0, final_video_duration))

output_video_path = os.path.join(output_folder, "final_video_shorts.mp4")
final_video.write_videofile(
    output_video_path, codec="libx264", audio_codec="aac", threads=4)
