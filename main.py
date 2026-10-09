from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# Frontend (PhanTee AI) ကနေ လှမ်းခေါ်ခွင့်ပြုရန် CORS ဖွင့်ပေးခြင်း
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
def extract_video(data: VideoRequest):
    # iOS Safari ရော Android ပါ တန်းဖွင့်လို့ရမည့် MP4 format သီးသန့် ဆွဲထုတ်ခြင်း
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=False)
            video_url = info.get('url')
            return {
                "success": True,
                "video_url": video_url,
                "title": info.get('title', 'Imported Video')
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))