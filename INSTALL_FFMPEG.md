# FFmpeg Installation Guide

FFmpeg is required to merge video and audio streams for 1080p downloads.

## Windows Installation

### Option 1: Using Chocolatey (Recommended)
```bash
choco install ffmpeg
```

### Option 2: Using Scoop
```bash
scoop install ffmpeg
```

### Option 3: Manual Installation
1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Download the "ffmpeg-release-essentials.zip" file
3. Extract the ZIP file to `C:\ffmpeg`
4. Add `C:\ffmpeg\bin` to your System PATH:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add `C:\ffmpeg\bin`
   - Click OK on all windows
5. Restart your terminal/command prompt

### Verify Installation
```bash
ffmpeg -version
```

## Linux Installation

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

### Fedora
```bash
sudo dnf install ffmpeg
```

### Arch Linux
```bash
sudo pacman -S ffmpeg
```

## macOS Installation

### Using Homebrew
```bash
brew install ffmpeg
```

## After Installation

1. Close and reopen your terminal
2. Verify FFmpeg is installed: `ffmpeg -version`
3. Restart the Flask application: `python app.py`
4. Try downloading again

## Why FFmpeg is Needed

YouTube serves 1080p video and audio as separate streams. FFmpeg merges them into a single MP4 file with both video and audio.
