"""
Transcript Gatherer for Knowledge Crawler
Automatically fetches and saves YouTube video transcripts
"""
import json
import os
import subprocess
from datetime import datetime

class TranscriptGatherer:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.base_path = "/home/workspace/MaatAI/borg_assimilation/knowledge_crawler"
        self.transcripts_path = os.path.join(self.base_path, channel_name, "transcripts")
        os.makedirs(self.transcripts_path, exist_ok=True)
    
    def gather_with_ytdlp(self, video_url, video_id):
        """Use yt-dlp to fetch transcript"""
        transcript_file = os.path.join(self.transcripts_path, f"{video_id}.txt")
        
        try:
            # Try to get transcript with yt-dlp
            cmd = [
                "yt-dlp",
                "--write-subs",
                "--write-auto-subs", 
                "--sub-lang",
                "en",
                "--skip-download",
                "--output",
                f"{self.transcripts_path}/{video_id}.%(ext)s",
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "video_id": video_id,
                    "transcript_file": transcript_file
                }
            else:
                return {
                    "status": "failed",
                    "video_id": video_id,
                    "error": result.stderr
                }
        except Exception as e:
            return {
                "status": "error",
                "video_id": video_id,
                "error": str(e)
            }
    
    def get_video_id(self, url):
        """Extract video ID from YouTube URL"""
        if "watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return None

def gather_code_bullet_transcripts():
    """Gather transcripts from Code Bullet videos"""
    gatherer = TranscriptGatherer("code_bullet")
    
    # Key videos to transcript
    videos = [
        ("https://www.youtube.com/watch?v=WSW-5m8lRMs", "flappy_bird_ai"),
        ("https://www.youtube.com/watch?v=tjQIO1rqTBE", "perfect_snake_ai"),
        ("https://www.youtube.com/watch?v=ehAStJmx_Fo", "minesweeper_ai"),
        ("https://www.youtube.com/watch?v=1g1HCYTX3Rg", "2048_ai"),
        ("https://www.youtube.com/watch?v=DZfv0YgLJ2Q", "chess_ai"),
        ("https://www.youtube.com/watch?v=qvpXpCvkqbc", "walk_3d_ai"),
    ]
    
    results = []
    for url, video_id in videos:
        print(f"📥 Gathering: {video_id}")
        result = gatherer.gather_with_ytdlp(url, video_id)
        results.append(result)
        print(f"   Status: {result['status']}")
    
    return results

def gather_oregon_trackers_transcripts():
    """Gather transcripts from Oregon Trackers videos"""
    gatherer = TranscriptGatherer("oregon_trackers")
    
    # Videos to transcript (from metadata)
    videos = [
        ("https://www.youtube.com/watch?v=8w4y2J2KjM8", "live_stream_full"),
    ]
    
    results = []
    for url, video_id in videos:
        print(f"📥 Gathering: {video_id}")
        result = gatherer.gather_with_ytdlp(url, video_id)
        results.append(result)
        print(f"   Status: {result['status']}")
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("TRANSCRIPT GATHERER - Knowledge Crawler")
    print("=" * 60)
    
    print("\n📺 Code Bullet Transcripts:")
    cb_results = gather_code_bullet_transcripts()
    
    print("\n📺 Oregon Trackers Transcripts:")
    ot_results = gather_oregon_trackers_transcripts()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Code Bullet: {sum(1 for r in cb_results if r['status'] == 'success')}/{len(cb_results)}")
    print(f"Oregon Trackers: {sum(1 for r in ot_results if r['status'] == 'success')}/{len(ot_results)}")
