"""
Sample video downloader for the Video Modification Bot.
This script downloads a sample video from Pixabay (royalty-free) for testing.
"""

import os
import requests
import shutil

def download_sample_video():
    """Download a sample video for testing."""
    print("Downloading sample video for testing...")
    
    # Create input directory if it doesn't exist
    os.makedirs("input_videos", exist_ok=True)
    
    # URL for the sample video (Creative Commons license)
    video_url = "https://cdn.pixabay.com/vimeo/149218360/stream.mp4?width=640&hash=5e796e83c95e79a3ebca5ec2670d1bc5a2e9a1e7"
    output_path = os.path.join("input_videos", "sample_video.mp4")
    
    try:
        # Download the video
        with requests.get(video_url, stream=True) as response:
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
        
        print(f"Sample video downloaded to {output_path}")
        print("You can now run the Video Modification Bot with: python main.py")
        return True
    except Exception as e:
        print(f"Error downloading sample video: {e}")
        return False

if __name__ == "__main__":
    download_sample_video()