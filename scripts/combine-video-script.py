#!/usr/bin/env python3
# scripts/combine_video.py
"""
Script to combine generated animation clips into a final 10-minute teaching
demonstration video with appropriate transitions.
"""

import os
import argparse
import subprocess
import glob
from pathlib import Path

def find_media_dir():
    """Find the media directory created by Manim."""
    possible_dirs = ["media", "output"]
    for dir_name in possible_dirs:
        if os.path.isdir(dir_name):
            return dir_name
    raise FileNotFoundError("Could not find media directory")

def get_video_files(quality="720p30"):
    """Get all rendered video files in the specified quality."""
    media_dir = find_media_dir()
    
    # Typical Manim output path structure
    videos_dir = os.path.join(media_dir, "videos")
    
    print(f"Looking for videos in {videos_dir}")
    # If using default Manim structure
    if os.path.isdir(videos_dir):
        # Find all scene directories
        scene_dirs = [d for d in os.listdir(videos_dir) if os.path.isdir(os.path.join(videos_dir, d))]
        print(f"Found {len(scene_dirs)} scene directories")
        video_files = []
        
        for scene_dir in scene_dirs:
            # Look for videos in the quality folder
            quality_dir = os.path.join(videos_dir, scene_dir, quality)
            print(f"Looking for videos in {quality_dir}")
            if os.path.isdir(quality_dir):
                print(f"Found {len(os.listdir(quality_dir))} video files")
                video_files.extend(glob.glob(os.path.join(quality_dir, "*.mp4")))
    else:
        # If using a flattened output structure
        video_files = glob.glob(os.path.join(media_dir, "**/*.mp4"), recursive=True)
    
    return video_files

def create_file_list(video_files, sequence_file=None):
    """
    Create a file list for ffmpeg to use with the concat demuxer.
    If a sequence file is provided, use it to order the videos.
    """
    # Create temporary file list
    list_file = "video_list.txt"
    
    # If a sequence file is provided, use it to order the videos
    if sequence_file and os.path.exists(sequence_file):
        ordered_files = []
        with open(sequence_file, 'r') as f:
            for line in f:
                scene_name = line.strip()
                if scene_name and not scene_name.startswith('#'):
                    # Find matching video file
                    matches = [f for f in video_files if scene_name.lower() in Path(f).stem.lower()]
                    if matches:
                        ordered_files.extend(matches)
        
        # Add any remaining files not specified in the sequence
        remaining = [f for f in video_files if f not in ordered_files]
        ordered_files.extend(remaining)
        
        video_files = ordered_files
    
    # Write file list
    with open(list_file, 'w') as f:
        for video_file in video_files:
            f.write(f"file '{os.path.abspath(video_file)}'\n")
    
    return list_file

def combine_videos(output_file="teaching_demo.mp4", sequence_file=None, quality="720p30"):
    """Combine all videos into a single file using ffmpeg."""
    video_files = get_video_files(quality)
    
    if not video_files:
        print("No video files found!")
        return
    
    print(f"Found {len(video_files)} video files to combine")
    
    # Create file list
    list_file = create_file_list(video_files, sequence_file)
    
    # Combine videos using ffmpeg
    cmd = [
        "ffmpeg", 
        "-y",  # Overwrite output file if it exists
        "-f", "concat", 
        "-safe", "0", 
        "-i", list_file, 
        "-c", "copy",
        output_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully combined videos into {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining videos: {e}")
    
    # Clean up temporary file
    os.remove(list_file)

def main():
    parser = argparse.ArgumentParser(description="Combine animation clips into final video")
    parser.add_argument("--output", "-o", default="teaching_demo.mp4", help="Output file name")
    parser.add_argument("--sequence", "-s", help="File containing the sequence of scenes to include")
    parser.add_argument("--quality", "-q", default="720p30", help="Video quality folder to use")
    
    args = parser.parse_args()
    
    combine_videos(args.output, args.sequence, args.quality)

if __name__ == "__main__":
    main()
