import asyncio
import json
import random
from playwright.async_api import async_playwright
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class FBClicker:
    def __init__(self, config_path="fb_config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.count = 0
        self.confirm_count = 0

    async def human_delay(self, min_sec=1, max_sec=3):
        await asyncio.sleep(random.uniform(min_sec, max_sec))

    async def clear_interruptions(self, page):
        """Dismisses calls, chat windows, and popups that block the screen."""
        try:
            # 1. Close Chat Windows (The little boxes at the bottom)
            chat_closes = await page.query_selector_all('[aria-label="Close chat"]')
            for btn in chat_closes:
                if await btn.is_visible():
                    await btn.click()
                    print("   💬 Closed a chat popupBox.")
            
            # 2. Decline/End Incoming Calls (The big overlays)
            # Facebook calls usually have "Decline" or "End call" buttons
            call_btns = await page.query_selector_all('[aria-label="Decline"]')
            call_btns += await page.query_selector_all('[aria-label="End call"]')
            call_btns += await page.query_selector_all('[aria-label="Close"]') # Sometimes it's just a general close
            
            for btn in call_btns:
                try:
                    # Specific check to see if it's inside a call-related layer
                    if await btn.is_visible():
                        await btn.click()
                        print("   ⛔ Dismissed an interruption/call.")
                except: continue

            # 3. General Popups (Not now, Dismiss, etc.)
            dismiss_text = ["Not now", "Dismiss", "Maybe later", "Close"]
            for text in dismiss_text:
                btns = await page.query_selector_all(f'text="{text}"')
                for btn in btns:
                    if await btn.is_visible():
                        await btn.click()
                        print(f"   🔔 Dismissed popup: {text}")
        except:
            pass

    async def click_buttons(self, page, only_confirm=False, only_add=False, limit=0):
        # Auto-clear any blocking popups first
        await self.clear_interruptions(page)
        
        print(f"\n🔍 Scanning for {'CONFIRM' if only_confirm else 'ADD FRIEND' if only_add else 'buttons'}...")
        
        round_clicks = 0
        
        # 1. Look for CONFIRM buttons
        if not only_add:
            confirms = await page.query_selector_all('div[role="button"]:has-text("Confirm")')
            confirms += await page.query_selector_all('[aria-label="Confirm"]')
            confirms += await page.query_selector_all('[aria-label="confirm"]')
            
            for btn in confirms:
                try:
                    if await btn.is_visible():
                        print("   🎯 Found CONFIRM button! Clicking...")
                        await btn.click()
                        self.confirm_count += 1
                        round_clicks += 1
                        await self.human_delay(2, 4)
                        if limit > 0 and round_clicks >= limit: return round_clicks
                        # Check for popups again after a click
                        await self.clear_interruptions(page)
                except: continue

        # 2. Look for ADD FRIEND
        if not only_confirm:
            adds = await page.query_selector_all('div[role="button"]:has-text("Add Friend")')
            adds += await page.query_selector_all('div[role="button"]:has-text("Add friend")')
            adds += await page.query_selector_all('[aria-label="Add Friend"]')
            adds += await page.query_selector_all('[aria-label="Add friend"]')
            
            for btn in adds:
                try:
                    if await btn.is_visible():
                        print("   👤 Found ADD FRIEND button! Clicking...")
                        await btn.click()
                        self.count += 1
                        round_clicks += 1
                        await self.human_delay(2, 4)
                        if limit > 0 and round_clicks >= limit: return round_clicks
                        # Check for popups again after a click
                        await self.clear_interruptions(page)
                except: continue
        
        return round_clicks

    async def run(self):
        print("\n" + "="*60)
        print("FACEBOOK STABLE CLICKER - HUMAN LOOP")
        print("="*60)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
            
            session_file = "fb_session.json"
            if os.path.exists(session_file):
                print(f"   📂 Loading saved session from {session_file}...")
                context = await browser.new_context(storage_state=session_file, viewport=None)
            else:
                print("   🆕 No saved session found. Starting fresh.")
                context = await browser.new_context(viewport=None)
                
            page = await context.new_page()
            try:
                await page.goto("https://www.facebook.com", wait_until="load", timeout=60000)
            except Exception as e:
                print(f"   ⚠️  Initial navigation error: {e}. Retrying...")
                await asyncio.sleep(5)
                await page.goto("https://www.facebook.com", wait_until="load", timeout=60000)
            
            # Check login status
            print("\n[1] Checking login status...")
            await asyncio.sleep(5)
            
            is_logged_in = False
            login_indicators = ['[aria-label="Home"]', 'div[role="navigation"]', '[aria-label="Your profile"]']
            
            for indicator in login_indicators:
                if await page.query_selector(indicator):
                    is_logged_in = True
                    print("   ✓ Already logged in!")
                    break
            
            if not is_logged_in:
                print("\n1. Please LOG IN manually.")
                print("2. Once you login, the bot will automatically SAVE your session.")
                # Wait for login detection
                max_wait = 300 # 5 minutes
                waited = 0
                while waited < max_wait and not is_logged_in:
                    await asyncio.sleep(5)
                    waited += 5
                    for indicator in login_indicators:
                        if await page.query_selector(indicator):
                            is_logged_in = True
                            print("\n   ✅ LOGIN DETECTED! Saving session...")
                            await context.storage_state(path=session_file)
                            print(f"   💾 Session saved to {session_file}")
                            break
                    if not is_logged_in:
                        print(f"   Waiting for login... ({waited}s)")

            if not is_logged_in:
                print("   ❌ Login timeout. Stopping.")
                await browser.close()
                return

            print("\n🚀 BOT ACTIVE!")
            
            try:
                loop_count = 0
                while True:
                    loop_count += 1
                    print(f"\n{'='*20} LOOP {loop_count} {'='*20}")

                    # --- STAGE 1: CONFIRM ALL REQUESTS ---
                    print(f"\n[STAGE 1] Navigating to Friend Requests...")
                    try:
                        await page.goto("https://www.facebook.com/friends/requests", wait_until="load", timeout=45000)
                        await asyncio.sleep(5)
                        
                        print("   🔍 Confirming all visible requests...")
                        await self.click_buttons(page, only_confirm=True)
                        print(f"   📊 Current: {self.confirm_count} Confirmed")
                    except Exception as e:
                        print(f"   ⚠️  Stage 1 Error (continuing): {e}")

                    # --- STAGE 2: ADD EXACTLY 4 FRIENDS (SUGGESTIONS) ---
                    print("\n[STAGE 2] Navigating to Friend Suggestions...")
                    try:
                        await page.goto("https://www.facebook.com/friends/suggestions", wait_until="load", timeout=45000)
                        await asyncio.sleep(5)

                        print("   🔍 Adding exactly 4 friends...")
                        await self.click_buttons(page, only_add=True, limit=4)
                        print(f"   📊 Progress: {self.count} Added, {self.confirm_count} Confirmed")
                    except Exception as e:
                        print(f"   ⚠️  Stage 2 Error (continuing): {e}")

                    # --- STAGE 3: HUMAN BREAK (HOME FEED SCROLL) ---
                    print("\n[STAGE 3] Human Behavior Simulation (Home Feed)...")
                    try:
                        await page.goto("https://www.facebook.com/", wait_until="load", timeout=45000)
                        await asyncio.sleep(5)

                        break_time_mins = random.uniform(1, 2)
                        print(f"   🌀 Scrolling home feed for {break_time_mins:.1f} minutes...")
                        
                        end_time = asyncio.get_event_loop().time() + (break_time_mins * 60)
                        while asyncio.get_event_loop().time() < end_time:
                            if page.is_closed(): break
                            # Random scroll amount
                            scroll_amount = random.randint(300, 700)
                            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
                            # Random pause between scrolls
                            await self.human_delay(5, 12)
                    except Exception as e:
                        print(f"   ⚠️  Stage 3 Error (continuing): {e}")
                    
                    print(f"\n✅ Loop {loop_count} complete. Restarting cycle...")

            except KeyboardInterrupt:
                print("\nStopped.")
            
            print("\nBrowser will stay open. Close it manually when done.")
            while not page.is_closed():
                await asyncio.sleep(10)

if __name__ == "__main__":
    bot = FBClicker()
    asyncio.run(bot.run())
