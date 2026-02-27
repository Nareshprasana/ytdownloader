#!/usr/bin/env python3
"""
YouTube Video Downloader Web Application
Flask-based web interface for downloading YouTube videos in 1080p
"""

from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import uuid
from pathlib import Path
import threading
import time

app = Flask(__name__)

# Configuration
DOWNLOAD_FOLDER = 'downloads'
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# Store download progress
download_status = {}


def get_video_info(url):
    """Extract video information without downloading"""
    ydl_opts = {
        'quiet': True, 
        'no_warnings': True,
        'format': '(bestvideo[vcodec^=vp9][height>=1440]/bestvideo[vcodec^=vp09][height>=1440]/bestvideo[height>=1440]/bestvideo[vcodec^=vp9][height>=1080]/bestvideo[vcodec^=vp09][height>=1080]/bestvideo[height>=1080]/bestvideo)+(bestaudio[acodec=opus]/bestaudio[acodec^=mp4a]/bestaudio)/best'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get the selected format info
            formats = info.get('formats', [])
            selected_format = info.get('format', 'Unknown')
            
            # Find highest quality formats with detailed info
            video_2k_vp9 = [f for f in formats if f.get('height') == 1440 and 'vp9' in str(f.get('vcodec', '')).lower()]
            video_2k = [f for f in formats if f.get('height') == 1440 and f.get('vcodec') != 'none']
            video_1080p_vp9 = [f for f in formats if f.get('height') == 1080 and 'vp9' in str(f.get('vcodec', '')).lower()]
            video_1080p = [f for f in formats if f.get('height') == 1080 and f.get('vcodec') != 'none']
            
            has_2k_vp9 = len(video_2k_vp9) > 0
            has_2k = len(video_2k) > 0
            has_1080p_vp9 = len(video_1080p_vp9) > 0
            has_1080p = len(video_1080p) > 0
            
            # Get best video quality info with bitrate
            best_height = 0
            best_fps = 0
            best_vcodec = 'Unknown'
            best_bitrate = 0
            best_acodec = 'Unknown'
            
            for f in formats:
                if f.get('vcodec') != 'none':
                    height = f.get('height', 0)
                    if height > best_height:
                        best_height = height
                        best_fps = f.get('fps', 0)
                        best_vcodec = f.get('vcodec', 'Unknown')
                        best_bitrate = f.get('tbr', 0)
            
            # Get best audio codec
            for f in formats:
                if f.get('acodec') != 'none':
                    best_acodec = f.get('acodec', 'Unknown')
                    if 'opus' in best_acodec.lower():
                        break
            
            return {
                'success': True,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'has_2k_vp9': has_2k_vp9,
                'has_2k': has_2k,
                'has_1080p_vp9': has_1080p_vp9,
                'has_1080p': has_1080p,
                'selected_format': selected_format,
                'resolution': info.get('resolution', 'Unknown'),
                'best_height': best_height,
                'best_fps': best_fps,
                'best_vcodec': best_vcodec,
                'best_bitrate': round(best_bitrate / 1000, 2) if best_bitrate else 0,
                'best_acodec': best_acodec
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def download_video(url, download_id):
    """Download video in background thread"""
    output_path = os.path.join(DOWNLOAD_FOLDER, download_id)
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            download_status[download_id] = {
                'status': 'downloading',
                'percent': d.get('_percent_str', '0%'),
                'speed': d.get('_speed_str', 'N/A'),
                'eta': d.get('_eta_str', 'N/A')
            }
        elif d['status'] == 'finished':
            download_status[download_id] = {
                'status': 'processing',
                'percent': '100%'
            }
    
    ydl_opts = {
        # Prioritize VP9 codec (highest quality on YouTube) with highest bitrate
        # VP9 at 1440p/1080p > AVC1 at 1440p/1080p > Best available
        'format': '(bestvideo[vcodec^=vp9][height>=1440]/bestvideo[vcodec^=vp09][height>=1440]/bestvideo[height>=1440]/bestvideo[vcodec^=vp9][height>=1080]/bestvideo[vcodec^=vp09][height>=1080]/bestvideo[height>=1080]/bestvideo)+(bestaudio[acodec=opus]/bestaudio[acodec^=mp4a]/bestaudio)/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mkv',  # MKV supports VP9 better than MP4
        'quiet': True,
        'no_warnings': True,
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
        'keepvideo': False,
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
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            download_status[download_id] = {
                'status': 'completed',
                'filename': os.path.basename(filename),
                'filepath': filename
            }
    except Exception as e:
        download_status[download_id] = {
            'status': 'error',
            'error': str(e)
        }


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/info', methods=['POST'])
def get_info():
    """Get video information"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    info = get_video_info(url)
    return jsonify(info)


@app.route('/api/download', methods=['POST'])
def start_download():
    """Start video download"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    download_id = str(uuid.uuid4())
    download_status[download_id] = {'status': 'starting'}
    
    # Start download in background thread
    thread = threading.Thread(target=download_video, args=(url, download_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'download_id': download_id})


@app.route('/api/status/<download_id>')
def get_status(download_id):
    """Get download status"""
    status = download_status.get(download_id, {'status': 'not_found'})
    return jsonify(status)


@app.route('/api/download/<download_id>')
def download_file(download_id):
    """Download the completed file"""
    status = download_status.get(download_id, {})
    
    if status.get('status') != 'completed':
        return jsonify({'error': 'File not ready'}), 404
    
    filepath = status.get('filepath')
    if filepath and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    
    return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    print("🚀 Starting YouTube Downloader Web App...")
    print("📱 Open your browser at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
