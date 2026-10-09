from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

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
        # YouTube Bot Check ကို ကျော်လွှားရန် Client များကို စုံလင်စွာ သတ်မှတ်ပေးခြင်း
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'mweb'],
                'player_skip': ['webpage', 'configs']
            }
        },
        'http_headers': {
            'User-Agent': 'com.google.ios.youtube/19.45.4 (iPhone16,2; U; CPU iOS 18_1 like Mac OS X; en_US)',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=False)
            video_url = info.get('url') or (info.get('entries', [{}])[0].get('url') if 'entries' in info else None)
            
            if not video_url:
                return {"success": False, "error": "Direct video stream URL not found"}
            
            return {
                "success": True,
                "video_url": video_url,
                "title": info.get('title', 'Imported Video'),
                "duration": info.get('duration', 0)
            }
    except Exception as e:
        return {"success": False, "error": str(e)}