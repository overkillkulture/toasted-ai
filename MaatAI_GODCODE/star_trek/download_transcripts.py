#!/usr/bin/env python3
"""
Voyager/DS9 Full Transcript Downloader (All Seasons)
Project: MaatAI / TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import asyncio
import aiohttp
import os
import re
from pathlib import Path
import json

BASE_URL = "https://subslikescript.com"
DS9_URL = f"{BASE_URL}/series/Star_Trek_Deep_Space_Nine-106145"
VOYAGER_URL = f"{BASE_URL}/series/Star_Trek_Voyager-112178"

async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                return await response.text()
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def extract_episode_links(session, series_url):
    html = await fetch_html(session, series_url)
    if not html:
        return []
    
    # subslikescript series pages list episodes as <a href="/series/Title-ID/season-X/episode-Y-Name">
    # We use regex to find them all
    pattern = r'href="(/series/[^"]+/season-\d+/episode-\d+-[^"]+)"'
    links = re.findall(pattern, html)
    # Deduplicate while preserving order
    unique_links = list(dict.fromkeys(links))
    return [f"{BASE_URL}{link}" for link in unique_links]

async def download_episode(session, url, output_dir, prefix):
    # Extract season and episode from URL
    match = re.search(r'season-(\d+)/episode-(\d+)', url)
    if not match:
        return False, f"Could not parse S/E from {url}"
    
    season, episode = match.groups()
    filename = f"{prefix}_s{season}e{episode}.txt"
    filepath = output_dir / filename
    
    if filepath.exists():
        return True, "Already exists"
        
    html = await fetch_html(session, url)
    if not html:
        return False, "Failed to fetch episode page"
        
    # Extract the main transcript text from <div class="full-script">
    script_match = re.search(r'<div class="full-script">(.*?)</div>', html, re.DOTALL)
    if not script_match:
        return False, "No script found on page"
        
    script_text = script_match.group(1)
    
    # Clean HTML tags
    script_text = re.sub(r'<br\s*/?>', '\n', script_text)
    script_text = re.sub(r'<[^>]+>', '', script_text)
    
    # Save file
    filepath.write_text(script_text.strip(), encoding='utf-8')
    return True, f"Saved {filename}"

async def main():
    output_dir = Path("/home/workspace/MaatAI/star_trek/transcripts")
    ds9_dir = output_dir / "ds9"
    voy_dir = output_dir / "voyager"
    
    ds9_dir.mkdir(parents=True, exist_ok=True)
    voy_dir.mkdir(parents=True, exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        print("Fetching DS9 episode list...")
        ds9_links = await extract_episode_links(session, DS9_URL)
        print(f"Found {len(ds9_links)} DS9 episodes.")
        
        print("Fetching Voyager episode list...")
        voy_links = await extract_episode_links(session, VOYAGER_URL)
        print(f"Found {len(voy_links)} Voyager episodes.")
        
        # Download in batches to avoid overwhelming the server
        batch_size = 10
        all_tasks = []
        
        for i, link in enumerate(ds9_links):
            all_tasks.append((link, ds9_dir, "ds9"))
        for i, link in enumerate(voy_links):
            all_tasks.append((link, voy_dir, "voyager"))
            
        success = 0
        errors = 0
        
        for i in range(0, len(all_tasks), batch_size):
            batch = all_tasks[i:i+batch_size]
            tasks = [download_episode(session, link, d, p) for link, d, p in batch]
            results = await asyncio.gather(*tasks)
            
            for ok, msg in results:
                if ok:
                    success += 1
                else:
                    errors += 1
            
            print(f"Progress: {min(i+batch_size, len(all_tasks))}/{len(all_tasks)} - Success: {success}, Errors: {errors}")
            await asyncio.sleep(1) # Polite delay

if __name__ == "__main__":
    asyncio.run(main())
