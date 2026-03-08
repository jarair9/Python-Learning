import os
import yt_dlp

VIDEOS_DIR = os.path.join(os.path.dirname(__file__), 'videos')
os.makedirs(VIDEOS_DIR, exist_ok=True)


def download_with_resolution(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title') or 'video'
        print(f"Title: {title}")

        # Show available resolutions (merged video+audio)
        formats = []
        for f in info.get('formats', []):
            # Check for formats that have both video and audio, or will be merged
            height = f.get('height')
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')
            
            # Include mp4 formats that have video
            if height and f.get('ext') == 'mp4' and vcodec != 'none':
                formats.append(f)
                # Mark if it has audio or needs merging
                has_audio = acodec != 'none'
                audio_status = "✓ audio" if has_audio else "needs merge"
                print(f"{len(formats)}. {height}p - {f.get('ext')} (id: {f.get('format_id')}) [{audio_status}]")

        if not formats:
            print("No mp4 formats found — downloading best available with audio.")
            ydl_opts = {
                'outtmpl': os.path.join(VIDEOS_DIR, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                # This ensures video+audio merged
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                ydl2.download([url])
            return

        try:
            choice = int(input("\nChoose resolution number: ")) - 1
            selected = formats[choice]
        except Exception:
            print("Invalid choice. Exiting.")
            return

        format_id = selected['format_id']
        
        # If selected format has no audio, merge with best audio
        if selected.get('acodec') == 'none':
            # Format: video_id+audio_id/best (fallback)
            format_spec = f"{format_id}+bestaudio[ext=m4a]/best[ext=mp4]"
            print(f"Will merge video ({format_id}) with best audio...")
        else:
            format_spec = format_id

        ydl_opts = {
            'format': format_spec,
            'outtmpl': os.path.join(VIDEOS_DIR, '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            # Ensure ffmpeg is used for merging (yt-dlp will auto-download if missing)
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
            ydl2.download([url])
        
        print(f"\nDownloaded to: {VIDEOS_DIR}")


if __name__ == '__main__':
    url = input("URL: ")
    download_with_resolution(url)