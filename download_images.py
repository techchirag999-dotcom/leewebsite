#!/usr/bin/env python3
"""
Lee Hydraulics & Fasteners — Image Cache Downloader
====================================================
Run this script ONCE after unzipping to download all website images
into an /images/ folder and rewrite index.html to use local paths.

Usage:
    python3 download_images.py

Requirements:
    pip install requests  (or uses built-in urllib)
"""

import os, re, time, urllib.request, urllib.error

HTML_FILE = "index.html"
IMG_DIR   = "images"

# All 21 unique Unsplash photos used in the site
IMAGES = {
    "photo-1504917595217-d4dc5ebe6122": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=1920&q=90&fit=crop&crop=center",
    "photo-1558618666-fcd25c85cd64":   "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=900&q=85&fit=crop&crop=center",
    "photo-1513828583688-c52646db42da": "https://images.unsplash.com/photo-1513828583688-c52646db42da?w=1200&q=85&fit=crop",
    "photo-1518709766631-a6a7f45921c3": "https://images.unsplash.com/photo-1518709766631-a6a7f45921c3?w=1200&q=85&fit=crop",
    "photo-1565043589221-1a6fd9ae45c7": "https://images.unsplash.com/photo-1565043589221-1a6fd9ae45c7?w=1920&q=85&fit=crop",
    "photo-1504328345606-18bbc8c9d7d1": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=700&q=85&fit=crop",
    "photo-1581092335397-9583eb92d232": "https://images.unsplash.com/photo-1581092335397-9583eb92d232?w=1920&q=85&fit=crop",
    "photo-1567789884554-0b844b597180": "https://images.unsplash.com/photo-1567789884554-0b844b597180?w=1920&q=85&fit=crop",
    "photo-1560250097-0b93528c311a":   "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=800&q=85&fit=crop&crop=top",
    "photo-1573496359142-b8d87734a5a2": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=500&q=80&fit=crop",
    "photo-1472099645785-5658abf4ff4e": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=500&q=80&fit=crop",
    "photo-1580489944761-15a19d654956": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=500&q=80&fit=crop",
    "photo-1534224039826-c7a0eda0e6b3": "https://images.unsplash.com/photo-1534224039826-c7a0eda0e6b3?w=1200&q=85&fit=crop",
    "photo-1557804506-669a67965ba0":   "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=500&q=80&fit=crop",
    "photo-1450101499163-c8848c66ca85": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=500&q=80&fit=crop",
    "photo-1581093458791-9d62f9098c4d": "https://images.unsplash.com/photo-1581093458791-9d62f9098c4d?w=600&q=80&fit=crop",
    "photo-1581092160607-ee22621dd758": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&q=80&fit=crop",
    "photo-1586528116311-ad8dd3c8310d": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=600&q=80&fit=crop",
    "photo-1611974789855-9c2a0a7236a3": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1920&q=85&fit=crop",
    "photo-1581091226033-d5c48150dbaa": "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=1920&q=85&fit=crop",
    "photo-1497366216548-37526070297c": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=85&fit=crop",
}

def download(pid, url, dest):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; site-builder/1.0)",
        "Accept": "image/webp,image/jpeg,image/*"
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)

def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    print(f"Downloading {len(IMAGES)} images into ./{IMG_DIR}/\n")

    downloaded = {}
    failed = []

    for i, (pid, url) in enumerate(IMAGES.items(), 1):
        fname = f"{pid}.jpg"
        dest  = os.path.join(IMG_DIR, fname)

        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            kb = os.path.getsize(dest) // 1024
            print(f"  {i:2d}/{len(IMAGES)}  SKIP (cached)  {pid[:28]}  {kb} KB")
            downloaded[pid] = fname
            continue

        try:
            kb = download(pid, url, dest) // 1024
            downloaded[pid] = fname
            print(f"  {i:2d}/{len(IMAGES)}  ✓  {pid[:28]}  {kb} KB")
            time.sleep(0.25)
        except Exception as e:
            failed.append(pid)
            print(f"  {i:2d}/{len(IMAGES)}  ✗  {pid[:28]}  ERROR: {e}")

    print(f"\nDownloaded: {len(downloaded)}/{len(IMAGES)}")

    if not downloaded:
        print("Nothing downloaded — keeping CDN URLs. Run again with internet access.")
        return

    # Rewrite index.html to use local paths
    print("\nRewriting index.html to use local image paths...")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    original = html
    replaced = 0
    for pid, fname in downloaded.items():
        # Replace all occurrences of this photo URL (any size/params) with local path
        pattern = re.compile(
            r'https://images\.unsplash\.com/' + re.escape(pid) + r'[^"\')\s]*'
        )
        local_path = f"images/{fname}"
        count = len(pattern.findall(html))
        html = pattern.sub(local_path, html)
        if count:
            print(f"  Replaced {count}x  {pid[:28]}  → {local_path}")
            replaced += count

    if replaced:
        # Backup original
        with open(HTML_FILE + ".bak", "w", encoding="utf-8") as f:
            f.write(original)
        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n✓ index.html updated ({replaced} URL replacements)")
        print(f"  Original backed up to index.html.bak")
    else:
        print("No replacements made.")

    if failed:
        print(f"\nFailed downloads ({len(failed)}) — CDN URLs kept for these:")
        for pid in failed:
            print(f"  {pid}")
        print("  Re-run the script with a stable internet connection.")

if __name__ == "__main__":
    main()
