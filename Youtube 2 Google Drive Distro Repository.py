import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
import googleapiclient.errors

def upload_video_to_youtube(file_path, title, description, category, privacy_status):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Set up OAuth2.0 authorization
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes)  # Update this to point to your client secret JSON file
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category  # Category should be passed as a string
            },
            "status": {
                "privacyStatus": privacy_status  # e.g., "public", "private", "unlisted"
            }
        },
        media_body=file_path  # Path to the video file
    )

    response = request.execute()
    return response['id']  # Returns the YouTube video ID

def upload_video_to_google_drive(file_path, title, description):
    scopes = ["https://www.googleapis.com/auth/drive.file"]  # Permission to access and upload to Google Drive

    # Set up OAuth2.0 authorization
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes)  # Path to your client secret JSON file
    credentials = flow.run_local_server(port=0)
    drive_service = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

    # Prepare file metadata and upload
    file_metadata = {
        'name': title,  # The title of the video on Google Drive
        'description': description,  # You can add a description here
        'mimeType': 'video/mp4'  # Assuming the file is an MP4 video
    }

    # Upload the file
    media = googleapiclient.http.MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
    request = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return request['id']  # Return the Google Drive file ID

def upload_video(file_path, title, description, category, privacy_status):
    youtube_video_id = upload_video_to_youtube(
        file_path=file_path,
        title=title,
        description=description,
        category=category,
        privacy_status=privacy_status
    )

    google_drive_file_id = upload_video_to_google_drive(
        file_path=file_path,
        title=title,
        description=description,
    )

    return youtube_video_id, google_drive_file_id

file_path = "FILE PATH OF VIDEO YOU WANT TO UPLOAD"
title = "[YOUR TITLE]"
description = "[YOUR DESCRIPTION]."
category = "[ADD NUMBER FOR CATEGORY CODE - SEE {https://mixedanalytics.com/blog/list-of-youtube-video-category-ids/} FOR REFERENCE]"
privacy_status = "[PRIVATE/PUBLIC/UNLISTED]"

youtube_video_id, google_drive_file_id = upload_video(
    file_path=file_path,
    title=title,
    description=description,
    category=category,
    privacy_status=privacy_status
)

print(f"YouTube Video ID: {youtube_video_id}")
print(f"Google Drive File ID: {google_drive_file_id}")