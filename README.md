# YouTube Video Downloader (Maximum Quality)

A web application to download YouTube videos in the absolute highest quality available with zero quality loss.

## Prerequisites

### FFmpeg Installation (Required)
FFmpeg is required to merge video and audio streams without any quality loss.

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (using Scoop):**
```bash
scoop install ffmpeg
```

**Windows (Manual):** See [INSTALL_FFMPEG.md](INSTALL_FFMPEG.md) for detailed instructions

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Application (Recommended)
1. Start the Flask server:
```bash
python app.py
```

2. Open your browser at: `http://localhost:5000`

3. Paste a YouTube URL, get video info, and download!

### Command Line (Alternative)
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Features

- 🎨 Beautiful, modern web interface
- 🏆 Downloads in MAXIMUM quality with VP9 codec (YouTube's highest quality format)
- 📊 Real-time download progress with speed and ETA
- 🖼️ Video preview with thumbnail and metadata
- 💾 100% lossless - stream copy with zero re-encoding
- 📱 Responsive design for mobile and desktop
- ⚡ Background download processing
- ✅ Shows codec, bitrate, and quality tier before downloading

## Quality Tiers

The app prioritizes formats in this order for maximum quality:

1. **🏆 PREMIUM QUALITY**: VP9 codec at 2K (1440p) - Highest bitrate, best compression
2. **⭐ HIGH QUALITY**: H.264 at 2K (1440p) - High bitrate
3. **✨ GOOD QUALITY**: VP9 codec at 1080p - Better than H.264 1080p
4. **📹 STANDARD QUALITY**: H.264 at 1080p
5. **📺 BASIC QUALITY**: Best available below 1080p

### Why VP9 is Better:
- VP9 provides 20-50% better compression than H.264 at the same quality
- YouTube uses VP9 for premium quality streams
- Higher bitrate = more detail preserved
- Opus audio codec (better than AAC)

## Zero Quality Loss Technology

- **Stream Copy**: Uses FFmpeg `-c:v copy -c:a copy` to copy streams without re-encoding
- **No Compression**: Original video and audio data preserved byte-for-byte
- **MKV Container**: Better support for VP9 codec than MP4
- **Bitrate Priority**: Always selects highest bitrate available

## How It Works

1. Paste a YouTube video URL
2. Click "Get Video Info" to preview the video
3. Check the quality badge:
   - 🏆 PREMIUM QUALITY (VP9 2K)
   - ⭐ HIGH QUALITY (2K)
   - ✨ GOOD QUALITY (VP9 1080p)
   - 📹 STANDARD QUALITY (1080p)
4. View codec, bitrate, and FPS information
5. Click "Download Video (Maximum Quality)" to start
6. Video downloads as MKV file with zero quality loss

## Troubleshooting

### Error: "ffmpeg is not installed"
- Install FFmpeg using the instructions above
- Restart your terminal after installation
- Verify with: `ffmpeg -version`
- Restart the Flask application

### Video downloads in lower quality
- Check the quality badge in the video info
- Some videos may not have VP9 or 2K available
- The app will automatically download the best available quality

### Why MKV instead of MP4?
- MKV has better support for VP9 codec
- No quality loss during container conversion
- Most modern players support MKV (VLC, Windows Media Player, etc.)
- If you need MP4, you can remux with: `ffmpeg -i video.mkv -c copy video.mp4`

## Notes

- Videos are downloaded in MKV format for maximum quality
- VP9 2K videos can be 3-8GB for a 10-minute video
- 100% lossless - exact same quality as YouTube's servers
- Downloads are saved to the `downloads/` folder
- The server runs on port 5000 by default
- Opus audio codec provides better quality than AAC at same bitrate
