from instagrapi import Client
import json
import os
import sys
import time
from typing import Optional, List, Dict

# --- THE ULTIMATE REELS FIX (Monkey Patch) ---
# Instagram changed their API to return 'null' for audio filters, 
# which crashes instagrapi's strict Pydantic validation.
# We force the clips_metadata to be a simple dict to skip strict validation.
try:
    import instagrapi.types
    from pydantic import ConfigDict
    
    # Patch the Media model's clips_metadata field to be a loose dict
    instagrapi.types.Media.model_fields['clips_metadata'].annotation = Optional[Dict]
    # Rebuild the model to apply changes
    instagrapi.types.Media.model_rebuild(force=True)
    print("REELS FIX: Successfully patched Media model for Reels compatibility.")
except Exception as e:
    print(f"REELS FIX: Warning: Patch application failed: {e}")

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Fix Pillow 10.0.0+ compatibility (ANTIALIAS was removed)
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

# Use relative path if video_folder_path is not absolute
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
        # Video is too wide, crop the sides
        new_width = clip.h * target_ratio
        x_start = (clip.w - new_width) / 2
        clip = clip.crop(x1=x_start, y1=0, x2=x_start + new_width, y2=clip.h)
    elif current_ratio < target_ratio:
        # Video is too tall, crop the top/bottom
        new_height = clip.w / target_ratio
        y_start = (clip.h - new_height) / 2
        clip = clip.crop(x1=0, y1=y_start, x2=clip.w, y2=y_start + new_height)
    
    # Finally resize to a standard Reel height (1080p)
    return clip.resize(height=1920)

def main():
    print("--- Genuine Instagram Reel Poster (v3 Pro) ---")
    
    cl = login_to_instagram()
    if not cl: return

    video_path, video_filename = get_next_video()
    if not video_path:
        print("No new videos found in folder.")
        return

    print(f"Processing: {video_filename}")
    
    caption = ""
    upload_success = False
    
    try:
        from moviepy.editor import VideoFileClip
        import moviepy.video.fx.all as vfx
        
        clip = VideoFileClip(video_path)
        duration = clip.duration
        
        # 1. Trim if longer than 90s
        if duration > 90:
            print(f"✂️ Trimming from {duration:.1f}s to 90s...")
            clip = clip.subclip(0, 90)
        
        # 2. Format to 9:16 (Optional, but makes it look like a pro Reel)
        print("📐 Formatting to 9:16 aspect ratio...")
        clip = format_video_for_reel(clip)
        
        # 3. Save processed video
        upload_path = os.path.join(os.path.dirname(video_path), "temp_reel.mp4")
        print("💾 Saving processed video...")
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

        print(f"🚀 Uploading as Reel... (Duration: {min(duration, 90):.1f}s)")
        
        # Use clip_upload - Reels ONLY (not in main feed/grid)
        media = cl.clip_upload(
            path=upload_path,
            caption=caption
        )
        print(f"✅ SUCCESS! Reel Posted (Reels Tab Only). Media ID: {media.pk}")
        
        # 4. Save History IMMEDIATELY on success
        with open('history.log', 'a', encoding='utf-8') as f:
            f.write(f"{video_filename}\n")
        upload_success = True
        
        # 5. Cleanup temp file (gracefully)
        if os.path.exists(upload_path):
            try:
                # Wait a second for file handle release
                time.sleep(2)
                os.remove(upload_path)
            except:
                pass
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        # Clean up if possible
        try:
            if 'clip' in locals(): clip.close()
            if 'upload_path' in locals() and os.path.exists(upload_path):
                time.sleep(2)
                os.remove(upload_path)
        except: pass
        return

if __name__ == "__main__":
    main()
