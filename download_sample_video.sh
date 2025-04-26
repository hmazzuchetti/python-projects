#!/bin/bash

# Sample video download script for testing the Video Modification Bot
# This script downloads a sample video from Pixabay (royalty-free) for testing purposes

echo "Downloading sample video for testing..."

# Create input directory if it doesn't exist
mkdir -p input_videos

# Download a sample video (Creative Commons license)
wget -O input_videos/sample_video.mp4 https://cdn.pixabay.com/vimeo/149218360/stream.mp4?width=640&hash=5e796e83c95e79a3ebca5ec2670d1bc5a2e9a1e7

echo "Sample video downloaded to input_videos/sample_video.mp4"
echo "You can now run the Video Modification Bot with: python main.py"
