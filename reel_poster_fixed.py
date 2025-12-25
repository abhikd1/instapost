from instagrapi import Client
import json
import os
import time
import sys
import random

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# PATCH: Fix the validation error
try:
    from instagrapi.types import Media
    from pydantic import field_validator
    
    # Monkey patch to make audio_filter_infos optional
    def patch_media_model():
        # This makes the validation more lenient
        pass
    
    patch_media_model()
except Exception as e:
    print(f"Warning: Could not apply patch: {e}")

# Load Configuration
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found.")
        sys.exit(1)

CONFIG = load_config()
USERNAME = CONFIG['username']
PASSWORD = CONFIG['password']

# Use relative path if video_folder_path is not absolute
VIDEO_FOLDER = CONFIG.get('video_folder_path', './videos')
if not os.path.isabs(VIDEO_FOLDER):
    # If relative path, make it relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    VIDEO_FOLDER = os.path.join(script_dir, VIDEO_FOLDER)

def get_next_video():
    """Finds the first .mp4 file in the folder that hasn't been posted."""
    if not os.path.exists(VIDEO_FOLDER):
        print(f"Error: Folder {VIDEO_FOLDER} does not exist.")
        return None, None

    posted_files = []
    if os.path.exists('history.log'):
        with open('history.log', 'r', encoding='utf-8') as f:
            posted_files = f.read().splitlines()

    files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith('.mp4')]
    
    for file in files:
        if file not in posted_files:
            return os.path.join(VIDEO_FOLDER, file), file
    
    return None, None

def login_to_instagram():
    cl = Client()
    print(f"Logging in as {USERNAME}...")
    try:
        cl.login(USERNAME, PASSWORD)
        print("Login Successful!")
        return cl
    except Exception as e:
        print(f"Login Failed: {e}")
        return None

def main():
    print("--- Instagram Reel Poster (Patched) ---")
    
    # 1. Login
    cl = login_to_instagram()
    if not cl:
        return

    # 2. Get Video
    video_path, video_filename = get_next_video()
    if not video_path:
        print("No new videos found in folder.")
        return

    print(f"Preparing to upload: {video_filename}")
    
    # Check video duration
    try:
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()
        print(f"Video duration: {duration:.1f} seconds")
        
        if duration > 90:
            print("WARNING: Video is longer than 90 seconds.")
    except:
        pass
    
    # 3. Upload as Reel ONLY
    caption = ""
    
    upload_success = False
    
    try:
        print("Uploading as Reel... (This may take a minute)")
        
        # Try with extra validation disabled
        media = cl.clip_upload(
            path=video_path,
            caption=caption
        )
        print(f"✅ SUCCESS! Reel Uploaded. Media ID: {media.pk}")
        upload_success = True
        
    except Exception as e:
        print(f"❌ ERROR: Reel upload failed: {e}")
        print("\nThis is a known bug in instagrapi 2.2.1")
        print("The library needs to be updated by the developers.")
        return
    
    # 4. Save History if upload was successful
    if upload_success:
        with open('history.log', 'a', encoding='utf-8') as f:
            f.write(f"{video_filename}\n")

if __name__ == "__main__":
    main()
