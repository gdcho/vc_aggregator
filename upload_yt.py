import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from concurrent.futures import ThreadPoolExecutor

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "yt_client_secret.json"
OAUTH_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, OAUTH_SCOPE)
    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    return youtube


def upload_video_to_youtube(youtube, file_path, title, description):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": description,
                "title": title
            },
            "status": {
                "privacyStatus": "private",
                "selfDeclaredMadeForKids": False,
                "publishAt": "2023-08-24T00:00:00.0Z"
            }
        },
        media_body=MediaFileUpload(
            file_path, mimetype='video/mp4', resumable=True)
    )
    return request.execute()


def get_only_video_from_folder(folder_path):
    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

    if len(video_files) == 1:
        return os.path.join(folder_path, video_files[0])
    else:
        print(
            f"Found {len(video_files)} video files in the folder. Expected only 1.")
        return None


def get_video_title_from_filepath(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def main():
    with ThreadPoolExecutor() as executor:
        youtube = executor.submit(authenticate_youtube).result()
        file_path = executor.submit(
            get_only_video_from_folder, "//Users/davidcho/vc_aggregator/output_folder").result()

    if file_path:
        title = get_video_title_from_filepath(file_path)
        description = ("Quick Unique Facts: "
                       "#quickuniquefacts #uniquefacts #funfacts "
                       "#interestingfacts #factoftheday #didyouknow "
                       "#knowledge #trivia #dailyfacts ")

        response = upload_video_to_youtube(
            youtube, file_path, title, description)
        print(response)
    else:
        print("Video upload aborted due to file path issues.")


if __name__ == "__main__":
    main()
