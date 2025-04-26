"""
Video editing module for the Video Modification Bot.
Handles adding captions and audio to videos using MoviePy.
"""

import os
import sys
from typing import Optional
# Updated imports for MoviePy 2.1.2
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

# Set up ImageMagick configuration
def configure_imagemagick():
    """
    Configure MoviePy to use ImageMagick by setting the path to the ImageMagick binary.
    This is needed for text operations in MoviePy.
    """
    # Common installation paths for ImageMagick on Windows
    possible_paths = [
        r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe",
        r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe", 
        r"C:\Program Files\ImageMagick-7.0.11-Q16-HDRI\magick.exe",
        r"C:\Program Files\ImageMagick-7.0.11-Q16\magick.exe"
    ]
    
    # Add generic version paths
    for version in range(0, 20):
        possible_paths.append(fr"C:\Program Files\ImageMagick-7.{version}.0-Q16-HDRI\magick.exe")
        possible_paths.append(fr"C:\Program Files\ImageMagick-7.{version}.0-Q16\magick.exe")
    
    # Check if any of these paths exist
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found ImageMagick at: {path}")
            os.environ["IMAGEMAGICK_BINARY"] = path
            return True
    
    print("Warning: ImageMagick not found at common paths.")
    print("Please install ImageMagick from: https://imagemagick.org/script/download.php#windows")
    print("Make sure to check 'Add application directory to your system path' during installation.")
    return False

# Try to configure ImageMagick when module is loaded
configure_imagemagick()

import config

def add_caption_to_video(video_path: str, caption_text: str, output_path: str = None) -> Optional[str]:
    """
    Add caption to a video.
    
    Args:
        video_path: Path to the input video file
        caption_text: Text to display as caption
        output_path: Path to save the output video (if None, a default path will be created)
        
    Returns:
        Path to the output video or None if processing fails
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} does not exist.")
        return None
    
    # If no output path is specified, create one in the output directory
    if not output_path:
        video_name = os.path.basename(video_path)
        name, ext = os.path.splitext(video_name)
        output_path = os.path.join(config.OUTPUT_VIDEOS_DIR, f"{name}_captioned{ext}")
    
    try:
        # Load the video clip
        video_clip = VideoFileClip(video_path)
        
        # Create a text clip for the caption
        txt_clip = TextClip(
            caption_text, 
            font_size=config.CAPTION_FONTSIZE,
            color=config.CAPTION_COLOR,
            stroke_color=config.CAPTION_STROKE_COLOR,
            stroke_width=config.CAPTION_STROKE_WIDTH,
            method='caption',
            # align='center',
            size=(video_clip.w * 0.9, None)  # Width is 90% of video width
        )
        
        # Set the position of the caption (fix for margin issue)
        if config.CAPTION_POSITION == "bottom":
            # Position at bottom with padding
            txt_position = ('center', video_clip.h - txt_clip.h - 20)
            txt_clip = txt_clip.set_position(txt_position)
        elif config.CAPTION_POSITION == "top":
            # Position at top with padding
            txt_position = ('center', 20)
            txt_clip = txt_clip.set_position(txt_position)
        else:  # center
            txt_clip = txt_clip.set_position('center')
        
        # Set the duration of the text clip to match the video
        txt_clip = txt_clip.set_duration(video_clip.duration)
        
        # Overlay the text clip on the video
        final_clip = CompositeVideoClip([video_clip, txt_clip])
        
        # Write the result to a file
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # Close the clips to release resources
        video_clip.close()
        final_clip.close()
        
        print(f"Caption added to video. Output saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error adding caption to video: {e}")
        print("\nThis error is likely because ImageMagick is not installed or configured properly.")
        print("Please install ImageMagick from: https://imagemagick.org/script/download.php#windows")
        print("Make sure to check 'Add application directory to your system path' during installation.")
        print("After installation, restart your terminal and try again.")
        return None

def add_audio_to_video(video_path: str, audio_path: str, output_path: str = None) -> Optional[str]:
    """
    Add audio to a video, replacing the original audio.
    
    Args:
        video_path: Path to the input video file
        audio_path: Path to the audio file to add
        output_path: Path to save the output video (if None, a default path will be created)
        
    Returns:
        Path to the output video or None if processing fails
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} does not exist.")
        return None
    
    if not os.path.exists(audio_path):
        print(f"Error: Audio file {audio_path} does not exist.")
        return None
    
    # If no output path is specified, create one in the output directory
    if not output_path:
        video_name = os.path.basename(video_path)
        name, ext = os.path.splitext(video_name)
        output_path = os.path.join(config.OUTPUT_VIDEOS_DIR, f"{name}_with_audio{ext}")
    
    try:
        # Load the video clip
        video_clip = VideoFileClip(video_path)
        
        # Load the audio clip
        audio_clip = AudioFileClip(audio_path)
        
        # If audio is longer than video, trim it
        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclip(0, video_clip.duration)
        
        # Set the audio of the video clip
        final_clip = video_clip.set_audio(audio_clip)
        
        # Write the result to a file
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # Close the clips to release resources
        video_clip.close()
        audio_clip.close()
        final_clip.close()
        
        print(f"Audio added to video. Output saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error adding audio to video: {e}")
        return None

def process_video(video_path: str, caption_text: str, audio_path: str, output_path: str = None) -> Optional[str]:
    """
    Process a video by adding both caption and audio.
    
    Args:
        video_path: Path to the input video file
        caption_text: Text to display as caption
        audio_path: Path to the audio file to add
        output_path: Path to save the final output video (if None, a default path will be created)
        
    Returns:
        Path to the output video or None if processing fails
    """
    # If no output path is specified, create one in the output directory
    if not output_path:
        video_name = os.path.basename(video_path)
        name, ext = os.path.splitext(video_name)
        output_path = os.path.join(config.OUTPUT_VIDEOS_DIR, f"{name}_processed{ext}")
    
    try:
        # First add caption to the video
        captioned_video = add_caption_to_video(video_path, caption_text)
        if not captioned_video:
            return None
        
        # Then add audio to the captioned video
        final_video = add_audio_to_video(captioned_video, audio_path, output_path)
        
        # Remove the intermediate captioned video to save space
        if os.path.exists(captioned_video) and captioned_video != video_path:
            os.remove(captioned_video)
            print(f"Removed intermediate file: {captioned_video}")
        
        return final_video
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return None

# For testing
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs(config.OUTPUT_VIDEOS_DIR, exist_ok=True)
    
    # This is just a placeholder for testing
    print("Video editor module loaded. Use the functions in this module to process videos.")
    print("Example usage:")
    print("  process_video('input.mp4', 'This is a caption', 'audio.mp3', 'output.mp4')")
