from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# Browser များမှ တိုက်ရိုက် ခေါ်ယူခွင့်ပြုရန် (မပါမဖြစ် လိုအပ်ပါသည်)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.post("/extract")
async def extract_video(req: VideoRequest):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {'player_client': ['android', 'ios']},
            'tiktok': {'app_version': 'latest'}
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=False)
            video_url = info.get('url') or (info.get('entries', [{}])[0].get('url') if 'entries' in info else None)
            
            if not video_url:
                return {"success": False, "error": "Direct video stream URL not found"}
            
            # Frontend က မျှော်လင့်နေသော format
            return {
                "success": True,
                "video_url": video_url,
                "title": info.get('title', 'Imported Video'),
                "duration": info.get('duration', 0)
            }
    except Exception as e:
        return {"success": False, "error": str(e)}