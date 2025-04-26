"""
Video selection module for the Video Modification Bot.
Handles selecting random videos from the input directory.
"""

import os
import random
from typing import List, Optional
import config

def get_video_files(directory: str = config.INPUT_VIDEOS_DIR) -> List[str]:
    """
    Get a list of all video files in the specified directory.
    
    Args:
        directory: Path to the directory containing video files
        
    Returns:
        List of video file paths
    """
    # Common video file extensions
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    
    video_files = []
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Warning: Directory {directory} does not exist.")
        return video_files
    
    # Get all files with video extensions
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            if ext.lower() in video_extensions:
                video_files.append(file_path)
    
    return video_files

def select_random_video(directory: str = config.INPUT_VIDEOS_DIR) -> Optional[str]:
    """
    Select a random video file from the specified directory.
    
    Args:
        directory: Path to the directory containing video files
        
    Returns:
        Path to the selected video file, or None if no videos are found
    """
    video_files = get_video_files(directory)
    
    if not video_files:
        print(f"No video files found in {directory}")
        return None
    
    # Select a random video
    selected_video = random.choice(video_files)
    print(f"Selected video: {os.path.basename(selected_video)}")
    
    return selected_video

# For testing
if __name__ == "__main__":
    video = select_random_video()
    if video:
        print(f"Successfully selected: {video}")
    else:
        print("No videos available for selection.")
