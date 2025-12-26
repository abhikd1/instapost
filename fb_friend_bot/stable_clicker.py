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

    async def click_buttons(self, page):
        print("\n🔍 Scanning for buttons...")
        
        # 1. Look for CONFIRM buttons first
        confirms = await page.query_selector_all('div[role="button"]:has-text("Confirm")')
        confirms += await page.query_selector_all('[aria-label="Confirm"]')
        confirms += await page.query_selector_all('[aria-label="confirm"]')
        
        found_confirm = False
        for btn in confirms:
            try:
                if await btn.is_visible():
                    print("   🎯 Found CONFIRM button! Clicking...")
                    await btn.click()
                    self.confirm_count += 1
                    found_confirm = True
                    await self.human_delay(2, 4)
            except: continue

        # 2. ONLY if no confirm buttons, look for ADD FRIEND
        if not found_confirm:
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
        print("FACEBOOK STABLE CLICKER")
        print("="*60)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
            context = await browser.new_context(viewport=None)
            page = await context.new_page()
            
            await page.goto("https://www.facebook.com")
            
            print("\n1. Please LOG IN manually.")
            print("2. Navigate to your list of people.")
            print("3. Stay on that page. The bot will start in 20 seconds.")
            
            for i in range(20, 0, -5):
                print(f"   Starting in {i}s...")
                await asyncio.sleep(5)
            
            print("\n🚀 BOT ACTIVE!")
            
            try:
                while True:
                    if page.is_closed(): break
                    
                    try:
                        await self.click_buttons(page)
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
