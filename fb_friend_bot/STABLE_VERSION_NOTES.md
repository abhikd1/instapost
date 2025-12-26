# Facebook Friend Bot - Stable Version Notes

## 🚀 Recommended Tool: `stable_clicker.py`
This is the most stable and reliable version of the bot. 

### **Why use this version?**
- **Prioritization:** It automatically clicks **"Confirm"** (Accept Request) buttons first.
- **Human-Like:** It skips "Add Friend" if "Confirm" buttons are on the screen, mimicking natural human prioritization.
- **Stability:** It manages browser windows more robustly to prevent unexpected closures.
- **Simplified Workflow:** It allows for manual login to bypass security checks, which is the safest way to avoid account flags.

### **How to Run:**
1. Open terminal in the `fb_friend_bot` folder.
2. Run: `python stable_clicker.py`
3. Log in manually within 20 seconds.

---

### **⚠️ IMPORTANT: MERGE WARNING**
**DO NOT MERGE this branch into the main codebase.**
This version uses a different logic and simplified architecture for stability. It is intended to run as a standalone stable tool. Merging it with the complex `run_bot_manual.py` or older logic will cause significant conflicts and may break existing persistent session handlers.
