import requests
from dotenv import load_dotenv
import os

load_dotenv()

tiktok_api_key = os.getenv("TIKTOK_API_KEY")

# Fetch TikTok posts
hashtag = 'your_hashtag'
url = f'https://api.tiktok.com/v2/challenge/detail/?challenge_id={hashtag}&access_key={tiktok_api_key}'
response = requests.get(url)
data = response.json()

for post in data['challenge']['view_data']:
    print(post['itemInfos']['text'])
