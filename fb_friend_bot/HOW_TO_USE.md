# Facebook Friend Bot - Assist Mode Guide

This bot helps you quickly add friends from a Facebook post's reaction list.

## 🚀 Quick Start

1.  **Stop any running bots/browsers.**
2.  **Open Terminal** in `fb_friend_bot` folder.
3.  **Run the command:**
    ```bash
    python run_bot_manual.py
    ```
4.  **Bot Actions:**
    -   It will open the Facebook post configured in `fb_config.json`.
    -   It will check if you are logged in (if not, log in manually).
    -   **YOU MUST**: Click the **Reactions Count** (the number next to Like/Love) to open the list of people.
    -   **YOU MUST**: Start **scrolling down** the list.
    -   **THE BOT WILL**: Automatically click "Add Friend" on anyone appearing in the list as you scroll.

## ⚙️ Configuration (`fb_config.json`)

To change the target post, edit `fb_config.json`:
```json
{
    "target_post_url": "https://www.facebook.com/share/p/YOUR_LINK_HERE/",
    "daily_request_limit": 100,
    ...
}
```

## ⚠️ Important Notes

-   **Manual Intervention**: You must open the list and scroll. The bot handles the clicking.
-   **Safety**: The bot waits 2-4 seconds between clicks to avoid blocks.
-   **Scanning**: You will see "Scanning..." in the terminal. This is normal. Just keep scrolling.
