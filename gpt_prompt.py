import openai
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
import IPython.display as ipd
from io import BytesIO

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
pexels_api_key = os.getenv("PEXELS_API_KEY")
openai.api_key = api_key

prompt = "Give me around 75 words based on an interesting fact."

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=200,
    stop=None
)

generated_fact = response.choices[0].text.strip()

print("Generated Fact:", generated_fact)

prompt2 = f"Based on the generated fact, {generated_fact}, return the one main subject noun."

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt2,
    max_tokens=30,
    stop=None
)

generated_keywords = response.choices[0].text.strip()

print("\nGenerated Keywords:", generated_keywords)

# Pexels - Fetch video data
pexels_url = f"https://api.pexels.com/videos/search?query={generated_keywords}&per_page=2"
headers = {"Authorization": pexels_api_key}
response = requests.get(pexels_url, headers=headers)
pexels_data = response.json()

if 'videos' in pexels_data:
    videos = pexels_data['videos']
    if videos:
        video = videos[0]
        print("Video URL:", video['url'])
        print("Video Title:", video['user']['name'])
    else:
        print("No videos found.")
else:
    print("No videos found in the response.")

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
