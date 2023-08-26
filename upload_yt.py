import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "yt_client_secret.json"  

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, ["https://www.googleapis.com/auth/youtube.upload"])
    
    credentials = flow.run_local_server(port=0)
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

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
        media_body=MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
    )
    response = request.execute()
    return response

if __name__ == "__main__":
    youtube = authenticate_youtube()
    file_path = "//Users/davidcho/vc_aggregator/output_folder/final_video_with_subtitles.mp4"
    title = "My YouTube Short"
    description = "This is a description for my YouTube Short."
    response = upload_video_to_youtube(youtube, file_path, title, description)
    print(response)
