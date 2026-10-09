# TikTok Data Backup Downloader

A Python script that turns TikTok's official data export into a local, date-organized video archive. Built in January 2025, two days before the U.S. TikTok ban took effect, to save my own favorited and saved videos before I lost access to them.

## Background

When the TikTok ban was set to take effect on January 19, 2025, I didn't want to lose years of saved videos, favorites, and collections. TikTok lets you request a copy of your account data, but the export only gives you **links** to videos, not the videos themselves.

So I requested my data (it took about a week to arrive), then wrote this script on January 17 to turn tens of thousands of links into actual video files before the deadline. Everything finished downloading before the ban went into effect.

Afterward I ran it as a small paid service for 4 other people who wanted their own TikTok data backed up.

## How it works

1. **Parse the export:** TikTok's data export includes a text file for each list (e.g., `Favorite Videos.txt`), where each entry is a `Date:` line followed by a `Link:` line. The script reads these in pairs and converts each date into a `datetime` object.
2. **Sort:** entries are sorted newest to oldest.
3. **Download:** each video is downloaded with [yt-dlp](https://github.com/yt-dlp/yt-dlp) in the best available quality.
4. **Name and organize:** files are saved as `YYYY-MM-DD_<videoID>.<ext>`, so the archive sorts chronologically in any file browser.
5. **Log failures:** videos that can't be downloaded (deleted, or set to private since being saved) are written to `skipped_links.txt` instead of crashing the run.

Running the script once per export file (favorites, likes, etc.) gives a separate archive for each category.

## Tech used

- Python 3
- yt-dlp (video downloading)
- `datetime` and `os` from the standard library (date parsing, file handling)

## How to run

1. Request your data from TikTok: **Settings → Account → Download your data**. Choose the TXT format. It can take several days to arrive.
2. Install the dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Put the export file (e.g., `Favorite Videos.txt`) in the same folder as the script.
4. Run:
   ```bash
   python download_tiktok_videos.py
   ```
   To use a different export file, pass it as an argument:
   ```bash
   python download_tiktok_videos.py "Liked Videos.txt"
   ```
5. Videos are saved to `Downloaded_Videos/`. Check `skipped_links.txt` for anything that failed.

## Results

- Archived tens of thousands of videos from my account before the January 19, 2025 deadline
- Handled deleted and private videos without stopping the run, and logged them for review
- Used the same script for 4 paying clients

## 2026 updates

I made three small fixes when I uploaded this project to GitHub in 2026:

- Blank lines in the export file no longer break the Date/Link pairing.
- Videos that were already downloaded are skipped, so an interrupted run can pick up where it stopped.
- The export file can be passed as a command-line argument (it still defaults to `Favorite Videos.txt`).

## What I'd do differently now

- **Better organization:** separate folders per category and more descriptive filenames (creator name, caption) instead of only date + video ID.
- **Rate limiting and retries:** add delays and automatic retries for temporary failures.
- **A front end:** I originally considered turning this into a simple web app so non-technical users could upload their export and get their videos back.

## Note

This tool is for backing up content from your own TikTok data export. Respect creators' rights and TikTok's Terms of Service.

© 2025 Roshan Kumar. All rights reserved. This code is shared for portfolio viewing only; no permission is granted to copy, modify, or distribute it.
