from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Fetch video data
search_query = 'your_search_query'
request = youtube.search().list(q=search_query, part='snippet', maxResults=10)
response = request.execute()

for item in response['items']:
    print(item['snippet']['title'])
    print(item['snippet']['description'])
