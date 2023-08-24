import os
import requests
import openai
import urllib.request
import textwrap
from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO
from googleapiclient.discovery import build
from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from pytube import YouTube
import ssl
from moviepy.editor import clips_array
from moviepy.config import change_settings
change_settings({"AUDIO_READING_FUNCTION": "pydub"})

ssl._create_default_https_context = ssl._create_unverified_context

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
load_dotenv()

OUTPUT_FOLDER = "//Users/davidcho/vc_aggregator/output_folder"
API_KEY = os.getenv("OPENAI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
openai.api_key = API_KEY
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def generate_fact():
    prompt = "Give me around 75 words based on an interesting fact."
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=200)
    return response.choices[0].text.strip()


def generate_subject_noun(fact):
    prompt = f"Based on the generated fact, {fact}, return a main subject noun."
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=30)
    return response.choices[0].text.strip()


def fetch_pexels_videos(keyword):
    url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=3"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers, timeout=30)
    return response.json().get('videos', [])


def fetch_youtube_videos(keyword):
    search_query = keyword + " free stock footage"
    request = youtube.search().list(q=search_query, part='snippet', maxResults=3)
    response = request.execute()
    return response.get('items', [])


def download_video_from_url(url, filename):
    urllib.request.urlretrieve(url, filename)


def get_tts_audio_clip(text):
    tts = gTTS(text, lang='en', tld='com.au', slow=False)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    temp_audio_filename = "temp_audio.mp3"
    with open(temp_audio_filename, "wb") as f:
        f.write(audio_bytes.read())
    audio_clip = AudioFileClip(temp_audio_filename)
    return audio_clip


def process_pexels_videos(pexels_videos, audio_clip_duration):
    video_clips = []
    for video_info in pexels_videos:
        video_files = video_info.get('video_files', [])
        if video_files:
            video_url = next(
                (file['link'] for file in video_files if file['file_type'] == 'video/mp4'), None)
            if video_url:
                video_filename = os.path.basename(
                    urllib.parse.urlparse(video_url).path)
                video_filename = os.path.join(OUTPUT_FOLDER, video_filename)
                download_video_from_url(video_url, video_filename)
                video_clip = VideoFileClip(video_filename)
                video_clip = video_clip.set_duration(audio_clip_duration // 3)
                video_clips.append(video_clip)
    return video_clips


def process_youtube_videos(youtube_videos, audio_clip_duration):
    video_clips = []
    for video_info in youtube_videos:
        video_id = video_info.get('id', {}).get('videoId')
        if video_id:
            youtube_video_url = f"https://www.youtube.com/watch?v={video_id}"
            yt = YouTube(youtube_video_url)
            video_stream = yt.streams.filter(
                progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            video_filename = os.path.join(
                OUTPUT_FOLDER, f"youtube_video_{video_id}.mp4")
            video_stream.download(output_path=OUTPUT_FOLDER,
                                  filename=os.path.basename(video_filename))
            video_clip = VideoFileClip(video_filename)
            video_clip = video_clip.set_duration(audio_clip_duration // 3)
            video_clips.append(video_clip)
    return video_clips


def generate_subtitles(fact, final_video_duration):
    fact_parts = textwrap.wrap(fact, width=40)
    subs = []
    interval_duration = 3
    start_time = 0
    for part in fact_parts:
        end_time = min(start_time + interval_duration, final_video_duration)
        subs.append(((start_time, end_time), part))
        start_time = end_time
    return subs


def annotate_video_with_subtitles(video, subtitles):
    def annotate(clip, txt, txt_color="white", fontsize=50, font="Xolonium-Bold"):
        txtclip = TextClip(txt, fontsize=fontsize, color=txt_color,
                           font=font, bg_color="black").set_duration(clip.duration)
        txtclip = txtclip.set_position(
            ("center", "center")).set_duration(clip.duration)
        cvc = CompositeVideoClip([clip, txtclip])
        return cvc

    annotated_clips = [annotate(video.subclip(from_t, min(
        to_t, video.duration)), txt) for (from_t, to_t), txt in subtitles]
    return concatenate_videoclips(annotated_clips)


def main():
    fact = generate_fact()
    noun = generate_subject_noun(fact)
    pexels_videos = fetch_pexels_videos(noun)
    youtube_videos = fetch_youtube_videos(noun)

    # Print results
    print(f"\nGenerated Fact: {fact}")
    print(f"\nGenerated Noun: {noun}\n")
    for video in pexels_videos:
        print(f"Pexel URL: {video['url']}")
    for video_info in youtube_videos:
        video_id = video_info['id'].get('videoId')
        if video_id:
            print(
                f"YouTube Video Link: https://www.youtube.com/watch?v={video_id}")

    # Process videos and audio
    audio_clip = get_tts_audio_clip(fact)
    audio_clip = audio_clip.volumex(1.0)
    print(f"Audio Duration: {audio_clip.duration} seconds")
    pexels_video_clips = process_pexels_videos(
        pexels_videos, audio_clip.duration)
    youtube_video_clips = process_youtube_videos(
        youtube_videos, audio_clip.duration)

    video_width = 1080
    video_height = 1920

    pexels_video_clips_resized = [clip.resize(
        (video_width, video_height)) for clip in pexels_video_clips]
    youtube_video_clips_resized = [clip.resize(
        (video_width, video_height)) for clip in youtube_video_clips]

    paired_clips = list(zip(pexels_video_clips_resized,
                        youtube_video_clips_resized))

    stacked_clips = [clips_array([[clip1], [clip2]])
                     for clip1, clip2 in paired_clips]

    final_video = concatenate_videoclips(stacked_clips, method="compose")

    final_video_duration = min(audio_clip.duration, final_video.duration)
    final_video = final_video.set_audio(
        audio_clip.subclip(0, final_video_duration))
    output_video_path = os.path.join(OUTPUT_FOLDER, "final_video_shorts.mp4")
    final_video.write_videofile(
        output_video_path, codec="libx264", audio_codec="aac", threads=4)

    subtitles = generate_subtitles(fact, final_video_duration)
    final_video_with_subs = annotate_video_with_subtitles(
        final_video, subtitles)
    final_video_with_subs = final_video_with_subs.set_audio(final_video.audio)
    output_video_with_subs_path = os.path.join(
        OUTPUT_FOLDER, "final_video_with_subtitles.mp4")
    final_video_with_subs.write_videofile(
        output_video_with_subs_path, codec="libx264", audio_codec="aac", threads=4)


if __name__ == "__main__":
    main()
