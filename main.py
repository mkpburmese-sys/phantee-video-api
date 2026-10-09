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
    # YouTube Bot Block ကျော်လွှားရန်
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'ios']
        },
        'tiktok': {
            'app_version': 'latest'
        }
    },
    # User-Agent အစစ် ထည့်သွင်းခြင်း
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
}