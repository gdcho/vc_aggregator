import openai
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
openai.api_key = api_key
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

prompt = "Give me around 75 words based on an interesting fact."

response = openai.Completion.create(
    engine="text-davinci-003",  
    prompt=prompt,
    max_tokens=200,  
    stop=None 
)

generated_fact = response.choices[0].text.strip()

print("Generated Fact:", generated_fact)

prompt2 = f"Based on the generated fact, {generated_fact}, give me three subjects."

response = openai.Completion.create(
    engine="text-davinci-003",  
    prompt=prompt2,
    max_tokens=30,  
    stop=None 
)

generated_keywords = response.choices[0].text.strip()

print("\nGenerated Keywords:", generated_keywords)

# YouTube - Fetch video data
search_query = f"{generated_keywords}" 
request = youtube.search().list(q=search_query, part='snippet', maxResults=10)
response = request.execute()

for item in response['items']:
    print(item['snippet']['title'])
    print(item['snippet']['description'])
