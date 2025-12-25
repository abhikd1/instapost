from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import json
import asyncio
from bot import FBFriendBot

app = FastAPI(title="Facebook Friend Bot API")
bot = FBFriendBot()
bot_task = None

class ConfigUpdate(BaseModel):
    fb_email: str = None
    fb_password: str = None
    target_post_url: str = None
    min_wait_seconds: int = None
    max_wait_seconds: int = None
    daily_request_limit: int = None
    scroll_pause_seconds: int = None

@app.get("/")
def read_root():
    return {
        "status": "Running" if bot.running else "Stopped",
        "requests_sent": bot.request_count,
        "message": "Facebook Friend Bot Control Panel"
    }

@app.post("/start")
async def start_bot(background_tasks: BackgroundTasks):
    global bot_task
    if bot.running:
        return {"error": "Bot is already running"}
    
    background_tasks.add_task(bot.run)
    return {"message": "Bot starting in background..."}

@app.post("/stop")
def stop_bot():
    if not bot.running:
        return {"error": "Bot is not running"}
    bot.stop()
    return {"message": "Bot stopping sign sent..."}

@app.get("/config")
def get_config():
    with open("fb_config.json", "r") as f:
        return json.load(f)

@app.post("/config/update")
def update_config(new_config: ConfigUpdate):
    with open("fb_config.json", "r") as f:
        current = json.load(f)
    
    # Update only provided fields
    for key, value in new_config.dict(exclude_unset=True).items():
        current[key] = value
        
    with open("fb_config.json", "w") as f:
        json.dump(current, f, indent=4)
        
    # Reload bot config
    bot.config = current
    return {"message": "Config updated and bot reloaded settings"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
