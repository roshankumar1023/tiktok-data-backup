#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 18:03:10 2025

@author: roshankumar
"""

import os
from yt_dlp import YoutubeDL
from datetime import datetime

# Define the file containing the TikTok links
file_name = "Favorite Videos.txt"

# Define the folder to save downloaded videos
output_folder = "Downloaded_Videos"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def download_video(video_url, output_folder, date):
    """Download a video from TikTok using yt-dlp and save it with date."""
    try:
        # Format date for filename (e.g., '2025-01-16')
        formatted_date = date.strftime("%Y-%m-%d")
        ydl_opts = {
            'outtmpl': os.path.join(output_folder, f'{formatted_date}_%(id)s.%(ext)s'),  # Save videos with date in filename
            'format': 'bestvideo+bestaudio/best',  # Get the best quality available
            'quiet': False,  # Show detailed logs
            'noplaylist': True  # Do not process playlists
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Downloaded: {video_url}")
        return True
    except Exception as e:
        print(f"Failed to download {video_url}: {e}")
        return False

def process_file(file_name):
    """Read the TikTok links from the file, sort by date, and download the videos."""
    skipped_links = []
    video_data = []

    try:
        with open(file_name, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        
        for i in range(0, len(lines) - 1, 2):  # Read pairs of Date and Link
            date_line = lines[i].strip()
            link_line = lines[i + 1].strip()

            if link_line.startswith("Link:"):
                video_url = link_line.split("Link: ")[1]
                
                try:
                    # Convert date to datetime object, including time
                    video_date = datetime.strptime(date_line, "Date: %Y-%m-%d %H:%M:%S")  # Full date format
                    video_data.append((video_date, video_url))
                except ValueError:
                    print(f"Skipping invalid date format: {date_line}")
        
        # Report how many videos were loaded
        if not video_data:
            print("No video URLs to process!")
        else:
            print(f"Loaded {len(video_data)} video(s). Sorting by date...")

        # Sort the list of videos by date (most recent first)
        video_data.sort(key=lambda x: x[0], reverse=True)

        # Download videos in sorted order
        for video_date, video_url in video_data:
            success = download_video(video_url, output_folder, video_date)
            if not success:
                skipped_links.append(video_url)

        # Log skipped links
        if skipped_links:
            with open("skipped_links.txt", "w") as skipped_file:
                skipped_file.write("\n".join(skipped_links))
            print("Some links could not be downloaded. Check skipped_links.txt.")
            
    except FileNotFoundError:
        print(f"The file {file_name} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the script
process_file(file_name)