import asyncio
import json
import random
import os
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
try:
    from playwright_stealth import stealth_async
except ImportError:
    # Fallback if stealth is not available
    async def stealth_async(page):
        pass

class FBFriendBot:
    def __init__(self, config_path="fb_config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.running = False
        self.request_count = 0
        self.page = None
        self.browser = None

    async def run(self):
        """Main bot execution flow"""
        self.running = True
        async with async_playwright() as p:
            try:
                # Step 1: Launch browser
                print("🚀 Step 1: Launching browser...")
                self.browser = await p.chromium.launch(
                    headless=False,
                    args=['--disable-blink-features=AutomationControlled']
                )
                context = await self.browser.new_context(
                    viewport={'width': 1280, 'height': 800},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                self.page = await context.new_page()
                await stealth_async(self.page)
                
                # Step 2: Login to Facebook
                await self.login()
                
                # Step 3: Navigate to the target post
                await self.navigate_to_post()
                
                # Step 4: Open reactions dialog
                await self.open_reactions()
                
                # Step 5: Send friend requests
                await self.send_friend_requests()
                
                print("✅ Bot completed successfully!")
                
            except Exception as e:
                print(f"❌ Error occurred: {str(e)}")
                import traceback
                traceback.print_exc()
            finally:
                if self.browser:
                    print("🔒 Closing browser...")
                    await asyncio.sleep(3)
                    await self.browser.close()

    async def login(self):
        """Step 2: Login to Facebook"""
        print("🔐 Step 2: Logging in to Facebook...")
        
        try:
            await self.page.goto("https://www.facebook.com/login", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            
            # Fill email
            print("   📧 Entering email...")
            await self.page.fill('input[name="email"]', self.config["fb_email"])
            await asyncio.sleep(0.5)
            
            # Fill password
            print("   🔑 Entering password...")
            await self.page.fill('input[name="pass"]', self.config["fb_password"])
            await asyncio.sleep(0.5)
            
            # Click login
            print("   👆 Clicking login button...")
            await self.page.click('button[name="login"]')
            
            # Wait for login to complete
            print("   ⏳ Waiting for login to complete...")
            await asyncio.sleep(8)
            
            # Check if login was successful
            current_url = self.page.url
            if "login" in current_url.lower():
                print("   ⚠️  Still on login page - may need manual intervention")
                await asyncio.sleep(10)  # Give time for 2FA or captcha
            else:
                print("   ✅ Login successful!")
                
        except Exception as e:
            print(f"   ❌ Login failed: {str(e)}")
            raise

    async def navigate_to_post(self):
        """Step 3: Navigate to the target post"""
        print(f"🎯 Step 3: Navigating to post...")
        print(f"   URL: {self.config['target_post_url']}")
        
        try:
            await self.page.goto(self.config["target_post_url"], wait_until="domcontentloaded")
            await asyncio.sleep(5)
            print("   ✅ Post page loaded!")
            
        except Exception as e:
            print(f"   ❌ Failed to navigate to post: {str(e)}")
            raise

    async def open_reactions(self):
        """Step 4: Open the reactions dialog"""
        print("❤️  Step 4: Opening reactions dialog...")
        
        try:
            # Try multiple selectors for the reactions count
            selectors = [
                'div[aria-label*="See who reacted"]',
                'span[role="button"]:has-text("Like")',
                'div[role="button"]:has-text("Like")',
                'span:has-text("Like")',
                # Generic reaction selector
                'div.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk. xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz',
            ]
            
            reaction_element = None
            for selector in selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements:
                        print(f"   ✅ Found {len(elements)} elements with selector: {selector[:50]}...")
                        reaction_element = elements[0]
                        break
                except:
                    continue
            
            if reaction_element:
                print("   👆 Clicking on reactions...")
                await reaction_element.click()
                await asyncio.sleep(3)
                print("   ✅ Reactions dialog should be open!")
            else:
                print("   ⚠️  Could not find reactions element automatically")
                print("   📝 Please manually click on the reactions count")
                print("   ⏳ Waiting 15 seconds for manual intervention...")
                await asyncio.sleep(15)
                
        except Exception as e:
            print(f"   ⚠️  Error opening reactions: {str(e)}")
            print("   📝 Please manually click on the reactions")
            print("   ⏳ Waiting 15 seconds for manual intervention...")
            await asyncio.sleep(15)

    async def send_friend_requests(self):
        """Step 5: Send friend requests to people who reacted"""
        print("👥 Step 5: Sending friend requests...")
        
        try:
            sent_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 50
            
            while self.running and sent_count < self.config["daily_request_limit"] and scroll_attempts < max_scroll_attempts:
                # Find all "Add Friend" buttons in the reactions dialog
                add_friend_buttons = await self.find_add_friend_buttons()
                
                if add_friend_buttons:
                    print(f"   🔍 Found {len(add_friend_buttons)} 'Add Friend' button(s)")
                    
                    # Click the first available button
                    try:
                        button = add_friend_buttons[0]
                        
                        # Scroll the button into view
                        await button.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        
                        # Check if visible
                        if await button.is_visible():
                            print(f"   👆 Clicking 'Add Friend' button #{sent_count + 1}...")
                            await button.click()
                            sent_count += 1
                            self.request_count += 1
                            print(f"   ✅ Friend request sent! Total: {sent_count}/{self.config['daily_request_limit']}")
                            
                            # Wait before next request
                            wait_time = random.randint(
                                self.config["min_wait_seconds"],
                                self.config["max_wait_seconds"]
                            )
                            print(f"   ⏳ Waiting {wait_time} seconds before next request...")
                            await asyncio.sleep(wait_time)
                        else:
                            print("   ⚠️  Button not visible, scrolling...")
                            await self.scroll_reactions_dialog()
                            
                    except Exception as e:
                        print(f"   ⚠️  Error clicking button: {str(e)}")
                        await self.scroll_reactions_dialog()
                else:
                    print("   🔍 No 'Add Friend' buttons found, scrolling...")
                    await self.scroll_reactions_dialog()
                    scroll_attempts += 1
                    await asyncio.sleep(self.config["scroll_pause_seconds"])
                
            print(f"   🎉 Finished! Sent {sent_count} friend requests")
            
        except Exception as e:
            print(f"   ❌ Error in send_friend_requests: {str(e)}")
            import traceback
            traceback.print_exc()

    async def find_add_friend_buttons(self):
        """Find all 'Add Friend' buttons on the current view"""
        try:
            # Multiple possible selectors for Add Friend button
            buttons = []
            
            # Try different text variations
            text_variations = [
                "Add Friend",
                "Add friend",
                "Add as Friend",
                "Confirm",
            ]
            
            for text in text_variations:
                try:
                    found = await self.page.get_by_role("button", name=text).all()
                    if found:
                        buttons.extend(found)
                except:
                    pass
            
            # Also try aria-label
            try:
                aria_buttons = await self.page.query_selector_all('div[aria-label="Add Friend"]')
                if aria_buttons:
                    buttons.extend(aria_buttons)
            except:
                pass
            
            # Remove duplicates
            unique_buttons = []
            for btn in buttons:
                if btn not in unique_buttons:
                    unique_buttons.append(btn)
            
            return unique_buttons
            
        except Exception as e:
            print(f"   ⚠️  Error finding buttons: {str(e)}")
            return []

    async def scroll_reactions_dialog(self):
        """Scroll within the reactions dialog to load more people"""
        try:
            # Try to find the scrollable container
            # The reactions dialog is usually in a specific div
            await self.page.mouse.wheel(0, 300)
            await asyncio.sleep(1)
        except Exception as e:
            print(f"   ⚠️  Error scrolling: {str(e)}")

    def stop(self):
        """Stop the bot"""
        print("🛑 Stopping bot...")
        self.running = False

if __name__ == "__main__":
    bot = FBFriendBot()
    asyncio.run(bot.run())
