# 🤖 Facebook Friend Bot - Version 3 (Human-Like Loop)

This bot is a highly stable, human-like automation tool for managing Facebook friend requests and growing your network safely.

## ✨ Key Features

1.  **Stage-Based Human Loop**:
    -   **Stage 1: Auto-Confirm** - Automatically navigates to your friend requests and confirms everyone.
    -   **Stage 2: Auto-Add** - Navigates to suggestions and adds exactly **4 friends** (to stay under the radar).
    -   **Stage 3: Home Scroll** - Mimics real browsing by scrolling the home feed for 1-2 minutes.
2.  **🛡️ Interruption Guard**:
    -   Automatically declines incoming calls.
    -   Closes chat popups and "Not now" dialogs.
    -   Ensures the bot never gets stuck on blocking layers.
3.  **Smart Session Management**:
    -   Saves your login state to `fb_session.json` so you don't have to log in every time.
4.  **Stealth Mode**: 
    -   Uses randomized human delays (3-12 seconds) between every action.

---

## 🚀 How to Use

### 1. Requirements
- Python 3.10+
- Playwright (`pip install playwright`)
- Browser installed (`playwright install chromium`)

### 2. Setup
1.  Make sure you have your credentials in `fb_config.json`:
    ```json
    {
      "email": "your_email@example.com",
      "password": "your_password"
    }
    ```

### 3. Running the Bot
1.  Open your terminal in the `fb_friend_bot` folder.
2.  Run:
    ```bash
    python stable_clicker.py
    ```
3.  **First Run**: If it's your first time, the bot will ask you to log in manually. Once you log in, it will save the session and handle everything automatically from then on.

---

## ⚙️ Configuration Hints
- The bot is tuned to click **4 people** per loop in Stage 2. This is the safest way to avoid "Action Blocked" warnings.
- It will repeat the cycle (Confirm -> Add -> Scroll) indefinitely until you stop it (`Ctrl+C`).

---

## ⚠️ Safety Warnings
- **Don't overdo it**: We recommend running this for a few hours a day rather than 24/7.
- **Account Age**: If your account is very new (less than 1 week), keep the limits even lower.
