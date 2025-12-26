# Facebook Bot - Version 3 (Human behavior loop)

This version focuses on mimicking natural human behavior by rotating between different sections of Facebook.

## 🔄 The Human Cycle (The Loop)

The bot now follows a 3-stage loop to avoid detection and act like a real person:

### **Stage 1: Process Requests (Confirm)**
- Automatically goes to `facebook.com/friends/requests`.
- **Logic:** Clicks ALL visible "Confirm" buttons on the screen.
- **Goal:** Clear pending incoming requests first.

### **Stage 2: Expand Network (Add Friend)**
- Automatically moves to `facebook.com/friends/suggestions`.
- **Constraint:** Clicks exactly **4 Add Friend** buttons, then stops.
- **Logic:** This avoids sending too many requests at once, which is a major red flag for Facebook.

### **Stage 3: Human Break (Home Feed)**
- Automatically navigates back to the **Facebook Home Feed**.
- **Action:** Scrolls down the feed randomly for **1 to 2 minutes**.
- **Logic:** Mimics a user reading their timeline. It uses random scroll amounts and random delays between scrolls (5-12 seconds).

---

## ✨ Key Technical Improvements
- **Precise Click Limits:** Added a `limit` parameter to ensure exactly 4 clicks in the "Add Friend" stage.
- **Smart Navigation:** Fully automated switching between URLs (`/requests` -> `/suggestions` -> `home`).
- **Resilient Polling:** If you close the browser, the script detects it and stops gracefully.

## 🚀 How to Run
1. Run `python stable_clicker.py`.
2. The bot will load your session automatically.
3. Sit back and watch it cycle through the stages! 

**⚠️ DO NOT MERGE:** This version is optimized for loop-based automation and differs significantly from previous versions.
