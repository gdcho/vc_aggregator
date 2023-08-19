import openai
from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
pexels_api_key = os.getenv("PEXELS_API_KEY")

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