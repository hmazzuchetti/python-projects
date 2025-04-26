"""
Main script for the Video Modification Bot.
Integrates all components to create a complete prototype.
"""

import os
import sys
import time
from dotenv import load_dotenv

# Import modules
import config
from video_selector import select_random_video
from text_generator import generate_text
from speech_generator import text_to_speech
from video_editor import process_video

def setup_environment():
    """Set up the environment for the bot."""
    # Create directories if they don't exist
    os.makedirs(config.INPUT_VIDEOS_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_VIDEOS_DIR, exist_ok=True)
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    # if not config.OPENAI_API_KEY:
    #     print("Warning: OpenAI API key not set. Please set it in the .env file or as an environment variable.")
    #     print("You can create a .env file in the project directory with the following content:")
    #     print("OPENAI_API_KEY=your_api_key_here")
    #     return False
    
    return True

def process_random_video():
    """Process a random video from the input directory."""
    print("\n=== Video Modification Bot ===")
    print("Starting video processing...")
    
    # Step 1: Select a random video
    print("\nStep 1: Selecting random video...")
    video_path = select_random_video()
    if not video_path:
        print("Error: No videos found in the input directory.")
        print(f"Please add some videos to {config.INPUT_VIDEOS_DIR}")
        return None
    
    # Step 2: Generate text
    print("\nStep 2: Generating motivational text...")
    caption_text = generate_text()
    if not caption_text:
        print("Error: Failed to generate text.")
        return None
    
    # Step 3: Convert text to speech
    print("\nStep 3: Converting text to speech...")
    audio_path = text_to_speech(caption_text)
    if not audio_path:
        print("Error: Failed to convert text to speech.")
        return None
    
    # Step 4: Process the video (add caption and audio)
    print("\nStep 4: Processing video (adding caption and audio)...")
    output_path = process_video(video_path, caption_text, audio_path)
    if not output_path:
        print("Error: Failed to process video.")
        return None
    
    print("\n=== Processing Complete ===")
    print(f"Original video: {os.path.basename(video_path)}")
    print(f"Generated caption: \"{caption_text}\"")
    print(f"Output video: {output_path}")
    
    return output_path

def main():
    """Main function to run the Video Modification Bot."""
    # Setup environment
    if not setup_environment():
        print("Environment setup incomplete. Please fix the issues and try again.")
        return
    
    # Check if input directory has videos
    if not os.listdir(config.INPUT_VIDEOS_DIR):
        print(f"No files found in the input directory: {config.INPUT_VIDEOS_DIR}")
        print("Please add some video files before running the bot.")
        return
    
    # Process a random video
    output_video = process_random_video()
    
    if output_video:
        print("\nVideo processing completed successfully!")
        print(f"The processed video is available at: {output_video}")
    else:
        print("\nVideo processing failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
