import asyncio
import json
import random
from playwright.async_api import async_playwright
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class InstaClicker:
    def __init__(self, config_path="insta_config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.follow_count = 0
        self.confirm_count = 0

    async def human_delay(self, min_sec=1, max_sec=3):
        await asyncio.sleep(random.uniform(min_sec, max_sec))

    async def click_buttons(self, page, only_confirm=False, only_follow=False, limit=0):
        print(f"\n🔍 Scanning for {'CONFIRM' if only_confirm else 'FOLLOW' if only_follow else 'buttons'}...")
        
        round_clicks = 0
        
        # 1. Look for CONFIRM/APPROVE buttons
        if not only_follow:
            # Instagram often uses "Confirm" or "Approve" for private account requests
            confirms = await page.query_selector_all('button:has-text("Confirm")')
            confirms += await page.query_selector_all('button:has-text("Approve")')
            
            for btn in confirms:
                try:
                    if await btn.is_visible():
                        print("   🎯 Found CONFIRM button! Clicking...")
                        await btn.click()
                        self.confirm_count += 1
                        round_clicks += 1
                        await self.human_delay(3, 6) # Insta is stricter, wait longer
                        if limit > 0 and round_clicks >= limit: return round_clicks
                except: continue

        # 2. Look for FOLLOW buttons
        if not only_confirm:
            follows = await page.query_selector_all('button:has-text("Follow")')
            # Exclude "Following" buttons
            follows = [f for f in follows if (await f.inner_text()).strip() == "Follow"]
            
            for btn in follows:
                try:
                    if await btn.is_visible():
                        print("   👤 Found FOLLOW button! Clicking...")
                        await btn.click()
                        self.follow_count += 1
                        round_clicks += 1
                        await self.human_delay(4, 8) # Insta is stricter
                        if limit > 0 and round_clicks >= limit: return round_clicks
                except: continue
        
        return round_clicks

    async def run(self):
        print("\n" + "="*60)
        print("INSTAGRAM STABLE CLICKER - HUMAN LOOP")
        print("="*60)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
            
            session_file = "insta_session.json"
            if os.path.exists(session_file):
                print(f"   📂 Loading saved session from {session_file}...")
                context = await browser.new_context(storage_state=session_file, viewport=None)
            else:
                print("   🆕 No saved session found. Starting fresh.")
                context = await browser.new_context(viewport=None)
                
            page = await context.new_page()
            await page.goto("https://www.instagram.com")
            
            # Check login status
            print("\n[1] Checking login status...")
            await asyncio.sleep(5)
            
            is_logged_in = False
            # Check for common post-login elements
            login_indicators = ['svg[aria-label="Home"]', 'svg[aria-label="New post"]', 'img[alt*="profile"]']
            
            for indicator in login_indicators:
                if await page.query_selector(indicator):
                    is_logged_in = True
                    print("   ✓ Already logged in!")
                    break
            
            if not is_logged_in:
                print("\n1. Please LOG IN to Instagram manually.")
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

            print("\n🚀 INSTA BOT ACTIVE!")
            
            try:
                loop_count = 0
                while True:
                    if page.is_closed():
                        print("\n   ⚠️  Page closed! Re-opening a new page...")
                        page = await context.new_page()

                    loop_count += 1
                    print(f"\n{'='*20} LOOP {loop_count} {'='*20}")

                    # --- STAGE 1: CONFIRM ACTIVITY ---
                    print(f"\n[STAGE 1] Navigating to Activity (Requests)...")
                    try:
                        await page.goto("https://www.instagram.com/accounts/activity/", wait_until="load", timeout=45000)
                        await asyncio.sleep(6) # Give it time to show buttons
                        
                        print("   🔍 Confirming visible requests...")
                        await self.click_buttons(page, only_confirm=True)
                        print(f"   📊 Current: {self.confirm_count} Confirmed")
                    except Exception as e:
                        print(f"   ⚠️  Stage 1 Error (continuing): {e}")

                    # --- STAGE 2: FOLLOW SUGGESTIONS ---
                    print("\n[STAGE 2] Navigating to Suggested People...")
                    try:
                        await page.goto("https://www.instagram.com/explore/people/", wait_until="domcontentloaded", timeout=45000)
                        await asyncio.sleep(8) # Recommendations take a while
                        
                        print("   🔍 Following exactly 4 suggested people...")
                        await self.click_buttons(page, only_follow=True, limit=4)
                        print(f"   📊 Progress: {self.follow_count} Followed, {self.confirm_count} Confirmed")
                    except Exception as e:
                        print(f"   ⚠️  Stage 2 Error (continuing): {e}")

                    # --- STAGE 3: HUMAN BREAK (FEED SCROLL) ---
                    print("\n[STAGE 3] Human Behavior Simulation (Instagram Feed)...")
                    try:
                        await page.goto("https://www.instagram.com/", wait_until="load", timeout=45000)
                        await asyncio.sleep(5)

                        break_time_mins = random.uniform(1.5, 3)
                        print(f"   🌀 Scrolling feed for {break_time_mins:.1f} minutes...")
                        
                        end_time = asyncio.get_event_loop().time() + (break_time_mins * 60)
                        while asyncio.get_event_loop().time() < end_time:
                            if page.is_closed(): break
                            # Instagram feed scrolling
                            scroll_amount = random.randint(400, 800)
                            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
                            await self.human_delay(8, 20)
                    except Exception as e:
                        print(f"   ⚠️  Stage 3 Error (continuing): {e}")
                    
                    print(f"\n✅ Loop {loop_count} complete. Restarting cycle...")

            except KeyboardInterrupt:
                print("\nStopped.")
            except Exception as e:
                print(f"\n🛑 Critical Error in run loop: {e}")
            
            print("\nBrowser will stay open. Close it manually when done.")
            while True:
                try:
                    if page.is_closed(): break
                    await asyncio.sleep(10)
                except: break

if __name__ == "__main__":
    bot = InstaClicker()
    asyncio.run(bot.run())
