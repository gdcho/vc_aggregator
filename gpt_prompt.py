import openai
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
import IPython.display as ipd
from io import BytesIO
from googleapiclient.discovery import build

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
    response = requests.get(pexels_url, headers=headers)
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
for videos in response['items']:
    print(
        f"YouTube Video Link: https://www.youtube.com/watch?v={videos['id']['videoId']}")

# gTTS - Text to Speech
tts = gTTS(generated_fact, lang='en', tld='com.au', slow=False)
audio_bytes = BytesIO()
tts.write_to_fp(audio_bytes)
audio_bytes.seek(0)

audio_filename = "generated_fact.mp3"
with open(audio_filename, "wb") as f:
    f.write(audio_bytes.read())

# Display and play audio
ipd.display(ipd.Audio(audio_filename, autoplay=True))
