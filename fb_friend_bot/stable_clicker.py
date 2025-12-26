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

    async def click_buttons(self, page, only_confirm=False, only_add=False):
        print("\n🔍 Scanning for buttons...")
        
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
                        await self.human_delay(2, 4)
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
                        await self.human_delay(2, 4)
                except: continue

    async def run(self):
        print("\n" + "="*60)
        print("FACEBOOK STABLE CLICKER - WITH SESSION")
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
            await page.goto("https://www.facebook.com")
            
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
                print("3. Navigate to your list of people.")
                
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
                # --- STAGE 1: CONFIRM REQUESTS ---
                print("\n[STAGE 1] Navigating to Friend Requests...")
                await page.goto("https://www.facebook.com/friends/requests")
                await self.human_delay(3, 5)
                
                print("   🔍 Confirming requests...")
                for _ in range(5): # Process 5 rounds of confirms
                    if page.is_closed(): break
                    await self.click_buttons(page, only_confirm=True)
                    print(f"   📊 Current: {self.confirm_count} Confirmed")
                    await page.evaluate("window.scrollBy(0, 500)")
                    await self.human_delay(2, 4)

                # --- STAGE 2: ADD FRIENDS (SUGGESTIONS) ---
                print("\n[STAGE 2] Navigating to Friend Suggestions...")
                await page.goto("https://www.facebook.com/friends/suggestions")
                await self.human_delay(3, 5)

                print("   🔍 Adding friends...")
                while True: # Continuous loop for suggestions
                    if page.is_closed(): break
                    
                    try:
                        await self.click_buttons(page, only_add=True)
                        print(f"   📊 Progress: {self.count} Added, {self.confirm_count} Confirmed")
                        
                        # Scroll down
                        await page.evaluate("window.scrollBy(0, 400)")
                        await self.human_delay(3, 5)
                    except Exception as e:
                        print(f"   Error in loop: {e}")
                        await asyncio.sleep(5)
            except KeyboardInterrupt:
                print("\nStopped.")
            
            print("\nBrowser will stay open. Close it manually when done.")
            while not page.is_closed():
                await asyncio.sleep(10)

if __name__ == "__main__":
    bot = FBClicker()
    asyncio.run(bot.run())
