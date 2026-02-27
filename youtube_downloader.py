#!/usr/bin/env python3
"""
YouTube Video Downloader
Downloads YouTube videos in 1080p quality (or best available)
"""

import yt_dlp
import sys


def download_video(url, output_path='downloads'):
    """
    Download a YouTube video in 1080p quality
    
    Args:
        url: YouTube video URL
        output_path: Directory to save the downloaded video
    """
    ydl_opts = {
        # Prioritize VP9 codec (highest quality on YouTube) with highest bitrate
        # VP9 at 1440p/1080p > AVC1 at 1440p/1080p > Best available
        'format': '(bestvideo[vcodec^=vp9][height>=1440]/bestvideo[vcodec^=vp09][height>=1440]/bestvideo[height>=1440]/bestvideo[vcodec^=vp9][height>=1080]/bestvideo[vcodec^=vp09][height>=1080]/bestvideo[height>=1080]/bestvideo)+(bestaudio[acodec=opus]/bestaudio[acodec^=mp4a]/bestaudio)/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mkv',  # MKV supports VP9 better than MP4
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [progress_hook],
        # Ensure absolutely no re-encoding or quality loss
        'postprocessor_args': [
            '-c:v', 'copy',      # Copy video stream without any re-encoding
            '-c:a', 'copy',      # Copy audio stream without any re-encoding
            '-map', '0:v:0',     # Map first video stream
            '-map', '0:a:0',     # Map first audio stream
            '-movflags', '+faststart',  # Optimize for streaming
            '-strict', 'experimental',
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,  # Delete intermediate files
        'writethumbnail': False,  # Don't save thumbnail
        'writesubtitles': False,  # Don't save subtitles
        'writeautomaticsub': False,  # Don't save auto-generated subtitles
        # Download highest bitrate available
        'format_sort': [
            'quality',
            'res:1440',
            'fps',
            'vcodec:vp9.2',
            'acodec:opus',
            'br',  # Bitrate
        ],
        'format_sort_force': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n📥 Downloading video from: {url}")
            info = ydl.extract_info(url, download=False)
            print(f"📹 Title: {info.get('title', 'Unknown')}")
            print(f"⏱️  Duration: {info.get('duration', 0) // 60} minutes")
            print(f"👤 Channel: {info.get('uploader', 'Unknown')}\n")
            
            ydl.download([url])
            print(f"\n✅ Download completed successfully!")
            print(f"📁 Saved to: {output_path}/")
            
    except Exception as e:
        print(f"\n❌ Error downloading video: {str(e)}")
        sys.exit(1)


def progress_hook(d):
    """Display download progress"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print(f"\n🔄 Processing video...")


def main():
    print("=" * 60)
    print("YouTube Video Downloader - 1080p Quality")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\n🔗 Enter YouTube video URL: ").strip()
    
    if not url:
        print("❌ No URL provided!")
        sys.exit(1)
    
    download_video(url)


if __name__ == "__main__":
    main()
