# Instagram Bot - Version 1 (Stable Human Loop)

This bot is a robust automation tool for Instagram, designed to mimic human browsing patterns while managing your social interactions. It utilizes a three-stage cycle to interact safely and effectively.

## 🚀 Core Features

### 🔑 1. Professional Session Management
- **One-Time Login:** Log in once manually, and the bot automatically saves your session to `insta_session.json`.
- **Persistent Access:** Future runs use saved cookies to bypass the login screen, keeping your credentials secure and reducing suspicious login attempts.

### 🧭 2. The Stable Human Loop
The bot operates in three distinct, automated stages to simulate a real user's workflow:

#### **Stage 1: Process Requests (Activity)**
- **URL:** `instagram.com/accounts/activity/`
- **Logic:** Navigates to your activity feed and automatically clicks all visible **"Confirm"** or **"Approve"** buttons.
- **Purpose:** Efficiently handles your incoming follow requests.

#### **Stage 2: Expand Network (Suggestions)**
- **URL:** `instagram.com/explore/people/`
- **Logic:** Identifies suggested profiles and performs exactly **4 Follow actions**.
- **Constraint:** Limited to 4 follows per loop to stay well within Instagram's safety limits.

#### **Stage 3: Authentic Feed Interaction (Break)**
- **URL:** `instagram.com/` (Home Feed)
- **Logic:** Scrolls through your home feed randomly for **1.5 to 3 minutes**.
- **Human Touch:** Uses randomized scroll amounts (400-800 pixels) and variable pauses (8-20 seconds) to mimic natural content consumption.

### 🛡️ 3. Advanced Stability & Safety
- **Robust Loading:** Uses `wait_until="load"` logic combined with ergonomic "buffer delays" (up to 8 seconds) to ensure all dynamic elements are visible before interaction.
- **Error Resiliency:** Features individual "Stage Guards" — if one section of Instagram fails to load, the bot logs the error and gracefully moves to the next stage instead of stopping.
- **Human-Like Timing:** Every click and scroll is preceded and followed by randomized delays.

---

## 🛠️ How to Get Started
1. Ensure your terminal is in the `insta_friend_bot` directory.
2. Run: `python insta_clicker.py`
3. If no session is found, follow the on-screen prompt to log in manually. 
4. The bot will handle the rest of the navigation and interaction automatically!

---

### ⚠️ Important Notice
This version is optimized for **standalone execution**. It maintains its own session and prevents account flags by strictly adhering to human-like behavior patterns.
