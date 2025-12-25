# Instagram Reel Auto-Poster

Automated Instagram Reel posting script with video processing capabilities.

## Features

- ✅ Automatic video trimming to 90 seconds
- ✅ Auto-format to 9:16 Reel aspect ratio
- ✅ Duplicate prevention with history tracking
- ✅ UTF-8 support for international filenames
- ✅ Reels-only posting (not in main feed)
- ✅ Automatic error handling and recovery

## Files

- `reel_poster.py` - Main manual posting script
- `auto_reel_bot.py` - Automated bot (60-80 min intervals)
- `config.json` - Instagram credentials and settings
- `history.log` - Posted videos tracking

## Setup

1. Install dependencies:
```bash
pip install instagrapi moviepy pillow
```

2. Configure `config.json`:
```json
{
  "username": "your_instagram_username",
  "password": "your_password",
  "video_folder_path": "path/to/your/videos"
}
```

3. Run the script:
```bash
# Manual posting (one at a time)
python reel_poster.py

# Automated posting (every 60-80 minutes)
python auto_reel_bot.py
```

## Requirements

- Python 3.8+
- instagrapi
- moviepy
- Pillow

## Usage

### Manual Mode
Place `.mp4` files in your video folder and run `reel_poster.py` whenever you want to post.

### Automated Mode
Run `auto_reel_bot.py` once and it will continuously post at random intervals (60-80 minutes).

## Notes

- Videos longer than 90 seconds are automatically trimmed
- All videos are formatted to 9:16 aspect ratio
- Posted videos are tracked in `history.log` to prevent duplicates
- Reels appear only in the Reels tab, not in main feed

## License

MIT License
