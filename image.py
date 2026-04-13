import yt_dlp

url = input("Url: ") # "https://stream.mux.com/hUT6X11m1Vkw1QMxPOLgI761x2cfpi9bHFbi5cNg4014.m3u8"


ydl_opts = {
    'outtmpl': 'video.mp4',
    'merge_output_format': 'mp4',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://stream.mux.com/',
        'Origin': 'https://stream.mux.com'
    },
    'quiet': False, 
    'no_warnings': False
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print("Download completed successfully!")
except Exception as e:
    print(f"Error: {e}")