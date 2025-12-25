import asyncio
import json
from playwright.async_api import async_playwright
import sys

# Ensure terminal can handle emojis/special chars
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class FBPrecisionBot:
    def __init__(self, config_path="fb_config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.count = 0

    async def run(self, post_url):
        async with async_playwright() as p:
            # Persistent context keeps you logged in
            user_data_dir = "./fb_user_data"
            context = await p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                no_viewport=True,
                viewport={'width': 1920, 'height': 1080},
                args=['--start-maximized', '--disable-blink-features=AutomationControlled']
            )
            page = context.pages[0] if context.pages else await context.new_page()
            
            # Apply Stealth
            try:
                from playwright_stealth import stealth_async
                await stealth_async(page)
            except ImportError:
                print("Stealth module not found, continuing without it.")

            print("\n" + "="*60)
            print("PRECISION FB BOT - SMART DIALOG MODE")
            print("="*60)

            # [1] Navigate
            print(f"[1] Opening Post: {post_url}")
            await page.goto(post_url)
            
            # [2] WAIT & SCAN LOOP
            print("\n[2] READY TO ASSIST:")
            print("   -> Manually open the reactions list.")
            print("   -> Scroll down the list.")
            print("   -> I will click 'Add Friend' whenever I see it.")
            
            processed = set()
            scan_count = 0
            
            while self.count < 100:
                # Find ALL buttons on the page that might be "Add Friend"
                # This covers dialogs, main page, anything.
                buttons = await page.locator('[aria-label="Add Friend"], [aria-label="Add friend"], [role="button"]:has-text("Add Friend")').all()
                
                if not buttons:
                    scan_count += 1
                    if scan_count % 10 == 0:
                        print(f"Scanning... (No buttons visible yet) [{scan_count}]")
                    await asyncio.sleep(1)
                    continue
                
                # Iterate and click
                for btn in buttons:
                    try:
                        if not await btn.is_visible(): continue
                        
                        # Get identifier to avoid duplicate clicks
                        # We use a unique property or just the handle
                        # For simple de-duping in this session, we try to grab a name nearby
                        # But simplest is just to click. 
                        
                        # Check if we already processed this element handle (tricky, so just rely on finding it)
                        # We can check if it says "Request sent" after clicking?
                        
                        txt = await btn.get_attribute("aria-label") or "Add Friend"
                        
                        # Click it!
                        print(f"   [CLICK] Found button: {txt}")
                        
                        # Use Javascript click for bypass
                        await btn.evaluate("el => el.click()")
                        
                        self.count += 1
                        
                        # Wait a bit
                        await asyncio.sleep(random.uniform(2, 4))
                        
                    except Exception as e:
                        # process might be detached
                        pass
                
                await asyncio.sleep(1)
            
            print(f"\nBATCH COMPLETE! Total Sent: {self.count}")
            await asyncio.sleep(5)
            await context.close()

if __name__ == "__main__":
    bot = FBPrecisionBot()
    # Read from config nicely
    if bot.config.get("target_post_url"):
        POST_URL = bot.config["target_post_url"]
    else:
        POST_URL = "https://www.facebook.com/share/p/1GphSv1f7v/"
    
    asyncio.run(bot.run(POST_URL))
