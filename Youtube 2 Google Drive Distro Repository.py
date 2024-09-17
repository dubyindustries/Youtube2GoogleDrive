import os
import tkinter as tk
from tkinter import filedialog, messagebox
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
import googleapiclient.errors

# Function to upload video to YouTube
def upload_video_to_youtube(file_path, title, description, category, privacy_status):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacy_status
            }
        },
        media_body=file_path
    )

    response = request.execute()
    return response['id']

# Function to upload video to Google Drive
def upload_video_to_google_drive(file_path, title, description):
    scopes = ["https://www.googleapis.com/auth/drive.file"]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes)
    credentials = flow.run_local_server(port=0)
    drive_service = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

    file_metadata = {
        'name': title,
        'description': description,
        'mimeType': 'video/mp4'
    }

    media = googleapiclient.http.MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
    request = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return request['id']

# Function to handle the video upload
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

# Function to select the file path
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

# Function to trigger the upload process
def start_upload():
    file_path = file_path_entry.get()
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    category = category_var.get()  # Get category from dropdown
    privacy_status = privacy_status_var.get()

    if not file_path or not title or not description or not category or not privacy_status:
        messagebox.showwarning("Missing Input", "Please fill out all fields.")
        return

    youtube_video_id, google_drive_file_id = upload_video(
        file_path=file_path,
        title=title,
        description=description,
        category=category,
        privacy_status=privacy_status
    )

    messagebox.showinfo("Upload Complete", f"Uploaded to YouTube: {youtube_video_id}\nUploaded to Google Drive: {google_drive_file_id}")

# Create the main window
window = tk.Tk()
window.title("YouTube2GoogleDrive")

# Set favicon (must be in .ico format)
window.iconbitmap("D:\Stream Stuff\YouTube\duby_industries\logo newest favicon_ICO.ico")  # Replace "favicon.ico" with your favicon file path

# Set background color and text color
window.configure(bg="black")

# Configure grid rows and columns
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# File path input
tk.Label(window, text="File Path:", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
file_path_entry = tk.Entry(window, width=40, bg="white", fg="black", insertbackground='white')
file_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
tk.Button(window, text="Browse", command=browse_file, bg="black", fg="white").grid(row=0, column=2, padx=10, pady=10)

# Title input
tk.Label(window, text="Title:", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
title_entry = tk.Entry(window, width=40, bg="white", fg="black", insertbackground='white')
title_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky="ew")

# Description input
tk.Label(window, text="Description:", bg="black", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
description_entry = tk.Text(window, width=40, height=5, bg="white", fg="black", insertbackground='white')
description_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="ew")

# Category input label and dropdown
tk.Label(window, text="Category:", bg="black", fg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
category_var = tk.StringVar(value="Select Category")
category_menu = tk.OptionMenu(window, category_var, 
    "Film & Animation", 
    "Film & Animation", 
    "Autos & Vehicles", 
    "Music", 
    "Pets & Animals", 
    "Sports", 
    "Travel & Events", 
    "Gaming", 
    "People & Blogs", 
    "Comedy", 
    "Entertainment", 
    "News & Politics", 
    "Education", 
    "Science & Technology")
category_menu.grid(row=3, column=1, padx=10, pady=10, sticky="w")
category_menu.config(bg="black", fg="white")

# Privacy Status input label and dropdown (aligned below Category)
tk.Label(window, text="Privacy Status:", bg="black", fg="white").grid(row=4, column=0, padx=10, pady=10, sticky="w")
privacy_status_var = tk.StringVar(value="Select Privacy Status")
privacy_status_menu = tk.OptionMenu(window, privacy_status_var, "private", "public", "unlisted")
privacy_status_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")
privacy_status_menu.config(bg="black", fg="white")

# Upload button
upload_button = tk.Button(window, text="Upload Video", command=start_upload, bg="black", fg="white")
upload_button.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

# Run the Tkinter event loop
window.mainloop()
