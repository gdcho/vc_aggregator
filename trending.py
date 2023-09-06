from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_youtube_service():
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
    API_VERSION = "v3"
    API_SERVICE_NAME = "youtube"

    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file("yt_client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def get_trending_videos(youtube):
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode="US",
        maxResults=5  
    )
    response = request.execute()

    for item in response["items"]:
        print(f"Title: {item['snippet']['title']}")
        print("-----")

if __name__ == "__main__":
    youtube = get_youtube_service()
    get_trending_videos(youtube)
