import asyncio
from bot_reactions import FBReactionBot

# Your target post
POST_URL = "https://www.facebook.com/share/p/1GphSv1f7v/"

print("=" * 60)
print("Facebook Friend Request Bot - Reaction Targeting")
print("=" * 60)
print(f"Target Post: {POST_URL}")
print("Settings: 2-5 min wait between requests")
print("Daily Limit: 30 requests")
print("=" * 60)
print("\nStarting bot...")
print("A browser window will open. DO NOT close it manually!")
print("=" * 60)

# Create and run the bot
bot = FBReactionBot()
asyncio.run(bot.run(POST_URL))

print("\n" + "=" * 60)
print("Bot finished successfully!")
print("=" * 60)
