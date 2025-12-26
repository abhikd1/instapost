# Facebook Bot - Version 2 (Stable Navigation)

This version of the bot includes advanced automation for Facebook friend management, focusing on stability and ease of use.

## ✨ Core Features

### 🔑 1. Session Persistence
- **Auto-Login:** The bot saves your login state to `fb_session.json` after the first manual login.
- **No Repeated Logins:** Future runs skip the login screen entirely by reloading your session cookies.

### 🧭 2. Automatic Two-Stage Navigation
The bot systematically handles your friend interactions by visiting specific Facebook sections:
- **Stage 1 (Requests):** Automatically visits `/friends/requests` to process all incoming "Confirm" requests.
- **Stage 2 (Suggestions):** Automatically moves to `/friends/suggestions` to send "Add Friend" requests to recommended profiles.

### 🤖 3. Intelligent Button Detection
- **Smart Selectors:** Identifies "Confirm" and "Add Friend" buttons using aria-labels, text matching, and role attributes.
- **Context Awareness:** Only clicks the relevant buttons for the current stage (Confirming vs. Adding).

### 🖱️ 4. Human-Like Behavior
- **Random Delays:** Mimics human timing between actions (2-4 seconds).
- **Auto-Scrolling:** Automatically scrolls down the page to load more content, just like a real user.

### 🛡️ 5. Enhanced Stability
- **Global Error Handling:** Wrapped in resilient loops to prevent the browser from closing on minor errors.
- **Manual Login Fallback:** If a session expires, the bot pauses and waits for you to log in manually before saving the new state.

---

## 🚀 How to Run
1. Navigate to the `fb_friend_bot` directory.
2. Run the command: `python stable_clicker.py`
3. If it's your first time, log in manually. The bot will handle the rest!

**Note:** This is a standalone stable tool. Do not merge with old versions to avoid logic conflicts.
