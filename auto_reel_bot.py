from instagrapi import Client
import json
import os
import sys
import time
import random
from typing import Optional, List, Dict
from datetime import datetime

# --- THE ULTIMATE REELS FIX (Monkey Patch) ---
try:
    import instagrapi.types
    from pydantic import ConfigDict
    
    instagrapi.types.Media.model_fields['clips_metadata'].annotation = Optional[Dict]
    instagrapi.types.Media.model_rebuild(force=True)
    print("REELS FIX: Successfully patched Media model for Reels compatibility.")
except Exception as e:
    print(f"REELS FIX: Warning: Patch application failed: {e}")

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Fix Pillow 10.0.0+ compatibility
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.Resampling.LANCZOS
except ImportError:
    pass

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

VIDEO_FOLDER = CONFIG.get('video_folder_path', './videos')
if not os.path.isabs(VIDEO_FOLDER):
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
        if file == "temp_reel.mp4": continue
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

def format_video_for_reel(clip):
    """Resizes/Crops video to 9:16 aspect ratio for Reels."""
    target_ratio = 9/16
    current_ratio = clip.w / clip.h
    
    if current_ratio > target_ratio:
        new_width = clip.h * target_ratio
        x_start = (clip.w - new_width) / 2
        clip = clip.crop(x1=x_start, y1=0, x2=x_start + new_width, y2=clip.h)
    elif current_ratio < target_ratio:
        new_height = clip.w / target_ratio
        y_start = (clip.h - new_height) / 2
        clip = clip.crop(x1=0, y1=y_start, x2=clip.w, y2=y_start + new_height)
    
    return clip.resize(height=1920)

def post_single_reel():
    """Posts a single reel and returns True if successful."""
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Reel Upload...")
    print(f"{'='*60}\n")
    
    cl = login_to_instagram()
    if not cl: 
        return False

    video_path, video_filename = get_next_video()
    if not video_path:
        print("No new videos found in folder.")
        return False

    print(f"Processing: {video_filename}")
    
    caption = ""
    upload_success = False
    
    try:
        from moviepy.editor import VideoFileClip
        
        clip = VideoFileClip(video_path)
        duration = clip.duration
        
        # Trim if longer than 90s
        if duration > 90:
            print(f"Trimming from {duration:.1f}s to 90s...")
            clip = clip.subclip(0, 90)
        
        # Format to 9:16
        print("Formatting to 9:16 aspect ratio...")
        clip = format_video_for_reel(clip)
        
        # Save processed video
        upload_path = os.path.join(os.path.dirname(video_path), "temp_reel.mp4")
        print("Saving processed video...")
        clip.write_videofile(
            upload_path, 
            codec="libx264", 
            audio_codec="aac", 
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True,
            verbose=False, 
            logger=None
        )
        clip.close()

        print(f"Uploading as Reel... (Duration: {min(duration, 90):.1f}s)")
        
        # Use clip_upload - Reels ONLY
        media = cl.clip_upload(
            path=upload_path,
            caption=caption
        )
        print(f"SUCCESS! Reel Posted (Reels Tab Only). Media ID: {media.pk}")
        
        # Save History IMMEDIATELY
        with open('history.log', 'a', encoding='utf-8') as f:
            f.write(f"{video_filename}\n")
        upload_success = True
        
        # Cleanup
        if os.path.exists(upload_path):
            try:
                time.sleep(2)
                os.remove(upload_path)
            except:
                pass
            
    except Exception as e:
        print(f"ERROR: {e}")
        try:
            if 'clip' in locals(): clip.close()
            if 'upload_path' in locals() and os.path.exists(upload_path):
                time.sleep(2)
                os.remove(upload_path)
        except: pass
        return False
    
    return upload_success

def run_bot():
    """Main bot loop - posts reels at random intervals."""
    print("\n" + "="*60)
    print("  INSTAGRAM REEL AUTO-POSTER BOT")
    print("  Posts every 60-80 minutes (random)")
    print("="*60 + "\n")
    
    post_count = 0
    
    while True:
        # Post a reel
        success = post_single_reel()
        
        if success:
            post_count += 1
            print(f"\nTotal Reels Posted: {post_count}")
        else:
            print("\nNo videos to post or upload failed.")
        
        # Calculate random wait time (60-80 minutes)
        wait_minutes = random.randint(60, 80)
        wait_seconds = wait_minutes * 60
        
        next_post_time = datetime.now()
        next_post_time = next_post_time.replace(
            hour=(next_post_time.hour + wait_minutes // 60) % 24,
            minute=(next_post_time.minute + wait_minutes % 60) % 60
        )
        
        print(f"\n{'='*60}")
        print(f"Waiting {wait_minutes} minutes until next post...")
        print(f"Next post scheduled at: {next_post_time.strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Wait with countdown
        for remaining in range(wait_seconds, 0, -60):
            mins = remaining // 60
            print(f"Time until next post: {mins} minutes...", end='\r')
            time.sleep(60)
        
        print("\n")

if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n\nBot stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n\nBot crashed: {e}")
