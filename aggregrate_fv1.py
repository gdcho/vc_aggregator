import openai
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
import IPython.display as ipd
from io import BytesIO
from googleapiclient.discovery import build
from moviepy.editor import AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import shutil
import urllib.request
import ssl
import pytube

ssl._create_default_https_context = ssl._create_unverified_context

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

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
    pexels_url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=2"
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
    for videos in response['items']:
        print(
            f"YouTube Video Link: https://www.youtube.com/watch?v={videos['id']['videoId']}")
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

# Build with MoviePy
pexels_videos = fetch_pexels_videos(generated_noun)
pexels_video_clips = []

for video_info in pexels_videos:
    video_files = video_info.get('video_files', [])
    
    if video_files:
        video_url = video_files[0].get('link', '')
        
        if video_url:
            video_filename = video_url.split('/')[-1]
            urllib.request.urlretrieve(video_url, video_filename)
            pexels_video_clip = VideoFileClip(video_filename)
            pexels_video_clips.append(pexels_video_clip)
            os.remove(video_filename)


youtube_video_clips = []
for video in response['items']:
    youtube_video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"

    yt = pytube.YouTube(youtube_video_url)
    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    video_filename = f"youtube_video_{video['id']['videoId']}.mp4"
    video_stream.download(output_path="", filename=video_filename)

    youtube_video_clip = VideoFileClip(video_filename)
    youtube_video_clips.append(youtube_video_clip)

# MoviePy text clip
text_clip = TextClip(generated_fact, fontsize=20, color='white').set_duration(60)

# Stack the Pexels and YouTube
stacked_pexels_videos = concatenate_videoclips(pexels_video_clips)
stacked_youtube_videos = concatenate_videoclips(youtube_video_clips)

# Combine video and text
final_video = CompositeVideoClip([text_clip.set_position('center'), stacked_pexels_videos.set_position('top'),
                                 stacked_youtube_videos.set_position('bottom')])

final_video = final_video.set_audio(tts_audio_clip)

output_video_path = "final_video.mp4"
final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

final_video.preview()

