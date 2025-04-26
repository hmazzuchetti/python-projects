"""
Video editing module for the Video Modification Bot using Pillow and OpenCV.
This is a replacement for the previous implementation that used MoviePy with ImageMagick.
"""

import os
import sys
from typing import Optional
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import config

def find_system_font(font_name=None):
    """
    Find a system font that can be used with Pillow.
    
    Args:
        font_name: Name of the font to look for (e.g., 'Arial', 'Impact')
                  If None, will try to use the font specified in config
    
    Returns:
        Path to the font file if found, None otherwise
    """
    if font_name is None:
        font_name = config.CAPTION_FONT
    
    # Common font directories and extensions to check
    font_dirs = [
        "/usr/share/fonts/truetype/",  # Linux
        "/usr/share/fonts/TTF/",       # Linux
        "/Library/Fonts/",             # macOS
        "C:\\Windows\\Fonts\\"         # Windows
    ]
    
    font_extensions = ['.ttf', '.otf', '.TTF', '.OTF']
    
    # Try exact name match first
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for ext in font_extensions:
                font_path = os.path.join(font_dir, f"{font_name}{ext}")
                if os.path.exists(font_path):
                    return font_path
    
    # Try case-insensitive partial match
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if any(file.lower().endswith(ext.lower()) for ext in font_extensions):
                        if font_name.lower() in file.lower():
                            return os.path.join(root, file)
    
    # Try some common fallback fonts
    fallback_fonts = [
        "DejaVuSans-Bold.ttf",
        "LiberationSans-Bold.ttf",
        "Arial.ttf",
        "Verdana.ttf",
        "TimesNewRoman.ttf",
        "Calibri.ttf"
    ]
    
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for fallback in fallback_fonts:
                for root, dirs, files in os.walk(font_dir):
                    for file in files:
                        if fallback.lower() in file.lower():
                            return os.path.join(root, file)
    
    print(f"Warning: Could not find font '{font_name}' or any suitable fallback.")
    return None

def add_caption_to_video(video_path: str, caption_text: str, output_path: str = None, word_by_word: bool = True, audio_duration: float = None) -> Optional[str]:
    """
    Add caption to a video using Pillow for text rendering and OpenCV for video processing.
    
    Args:
        video_path: Path to the input video file
        caption_text: Text to display as caption
        output_path: Path to save the output video (if None, a default path will be created)
        word_by_word: If True, display one word at a time with animation
        audio_duration: Duration of the audio in seconds, used for timing the words (if None, will use video duration)
        
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
        # Open the video file with OpenCV
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return None
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = frame_count / fps
        
        # Calculate the number of additional frames for 3-second buffer
        buffer_seconds = 3.0
        buffer_frames = int(buffer_seconds * fps)
        new_frame_count = frame_count + buffer_frames
        
        print(f"Original video duration: {video_duration:.2f} seconds ({frame_count} frames)")
        print(f"Adding {buffer_seconds} seconds buffer ({buffer_frames} frames)")
        print(f"New video duration: {(video_duration + buffer_seconds):.2f} seconds ({new_frame_count} frames)")
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v codec
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Find a suitable font
        font_path = find_system_font(config.CAPTION_FONT)
        font_size = config.CAPTION_FONTSIZE
        
        # Load font
        if (font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                print(f"Using font: {font_path}")
            except Exception as e:
                print(f"Error loading font: {e}. Using default font.")
                font = ImageFont.load_default()
        else:
            font = ImageFont.load_default()
            print("Using default font")
        
        # Convert colors from config
        # Note: Pillow uses RGB, but config might be in different format
        if isinstance(config.CAPTION_COLOR, str):
            # Convert color name to RGB
            color_map = {
                "white": (255, 255, 255),
                "black": (0, 0, 0),
                "red": (255, 0, 0),
                "green": (0, 255, 0),
                "blue": (0, 0, 255),
                "yellow": (255, 255, 0),
                "cyan": (0, 255, 255),
                "magenta": (255, 0, 255)
            }
            text_color = color_map.get(config.CAPTION_COLOR.lower(), (255, 255, 255))
        else:
            # Assume it's already an RGB tuple
            text_color = config.CAPTION_COLOR
        
        # Same for stroke color
        if isinstance(config.CAPTION_STROKE_COLOR, str):
            color_map = {
                "white": (255, 255, 255),
                "black": (0, 0, 0),
                "red": (255, 0, 0),
                "green": (0, 255, 0),
                "blue": (0, 0, 255),
                "yellow": (255, 255, 0),
                "cyan": (0, 255, 255),
                "magenta": (255, 0, 255)
            }
            stroke_color = color_map.get(config.CAPTION_STROKE_COLOR.lower(), (0, 0, 0))
        else:
            stroke_color = config.CAPTION_STROKE_COLOR
        
        print(f"Processing video with {frame_count} frames plus {buffer_frames} buffer frames...")
            
        # For word-by-word animation
        if word_by_word:
            # Split the caption into words
            words = caption_text.split()
            num_words = len(words)
            
            # Use audio duration if provided, otherwise use video duration
            # But ensure we use at least the video duration to prevent cutting the video
            # Add buffer seconds to ensure text doesn't get cut at the end
            duration_to_use = video_duration
            if audio_duration is not None:
                # Make sure we're using the longer of video or audio duration
                duration_to_use = max(video_duration, audio_duration)
                
            # Add buffer for text display
            text_display_duration = duration_to_use + buffer_seconds
            print(f"Using duration: {text_display_duration:.2f} seconds for {num_words} words")
            
            # Calculate how many frames each word should appear
            # Each word gets an equal portion of the total duration
            seconds_per_word = text_display_duration / num_words
            frames_per_word = int(seconds_per_word * fps)
            
            # Ensure minimum visibility (at least 0.3 seconds per word)
            min_frames = max(5, int(0.3 * fps))
            if frames_per_word < min_frames:
                frames_per_word = min_frames
                print(f"Adjusted to minimum {frames_per_word} frames per word")
                
            # Calculate fade-in and fade-out frames (15% of word time for each transition)
            fade_frames = max(2, int(frames_per_word * 0.15))
            
            print(f"Each word will display for {frames_per_word} frames ({frames_per_word/fps:.2f} seconds)")
            print(f"Fade in/out: {fade_frames} frames ({fade_frames/fps:.2f} seconds)")
            
            # Process each frame
            frame_number = 0
            current_word_index = -1
            current_word = ""
            word_frame_count = 0
            
            # Process original video frames
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                frame_number += 1
                if frame_number % 100 == 0 or frame_number == 1:
                    print(f"Processing frame {frame_number}/{new_frame_count}")
                
                # Determine which word to show
                word_frame_count += 1
                if word_frame_count > frames_per_word:
                    word_frame_count = 1
                    current_word_index += 1
                    if current_word_index >= len(words):
                        current_word_index = len(words) - 1  # Stay on last word instead of looping
                    current_word = words[current_word_index]
                
                # Calculate alpha (transparency) for fade effect
                alpha = 255  # Full opacity
                if word_frame_count <= fade_frames:  # Fade in
                    alpha = int(255 * (word_frame_count / fade_frames))
                elif word_frame_count > frames_per_word - fade_frames:  # Fade out
                    alpha = int(255 * ((frames_per_word - word_frame_count) / fade_frames))
                
                # Ensure alpha is within bounds
                alpha = max(0, min(255, alpha))
                
                # Create a sample image to measure current word dimensions
                sample_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                sample_draw = ImageDraw.Draw(sample_img)
                text_bbox = sample_draw.textbbox((0, 0), current_word, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Center the text both horizontally and vertically
                text_x = (width - text_width) // 2
                text_y = (height - text_height) // 2
                
                # Convert OpenCV BGR to RGB for Pillow
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Create a Pillow Image from the frame
                pil_image = Image.fromarray(rgb_frame)
                
                # Create a transparent overlay for the background
                overlay = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                
                # Add semi-transparent background for better readability
                background_padding = 10
                background_x1 = text_x - background_padding
                background_y1 = text_y - background_padding
                background_x2 = text_x + text_width + background_padding
                background_y2 = text_y + text_height + background_padding
                
                # Draw semi-transparent background with fade effect
                background_alpha = min(128, alpha // 2)  # Half the text opacity for background
                overlay_draw.rectangle(
                    [background_x1, background_y1, background_x2, background_y2],
                    fill=(0, 0, 0, background_alpha)  # Black with variable opacity
                )
                
                # Convert PIL image to RGBA if it's not already
                if pil_image.mode != 'RGBA':
                    pil_image = pil_image.convert('RGBA')
                    
                # Composite the overlay onto the image
                pil_image = Image.alpha_composite(pil_image, overlay)
                
                # Draw text with stroke (outline) and adjusted opacity
                draw = ImageDraw.Draw(pil_image)
                text_color_with_alpha = text_color + (alpha,)  # Add alpha to RGB
                stroke_color_with_alpha = stroke_color + (alpha,)  # Add alpha to RGB
                
                draw.text(
                    (text_x, text_y),
                    current_word,
                    font=font,
                    fill=text_color_with_alpha,
                    stroke_width=config.CAPTION_STROKE_WIDTH,
                    stroke_fill=stroke_color_with_alpha
                )
                
                # Convert back to OpenCV format (RGB to BGR)
                cv_frame = cv2.cvtColor(np.array(pil_image.convert('RGB')), cv2.COLOR_RGB2BGR)
                
                # Write the frame to the output video
                out.write(cv_frame)
            
            # Get the last frame to duplicate for buffer
            if frame_number > 0:
                # Reset cap to get the last frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
                ret, last_frame = cap.read()
                
                if ret:
                    print(f"Adding {buffer_frames} buffer frames using last frame...")
                    
                    # Add buffer frames using the last frame
                    for i in range(buffer_frames):
                        frame_number += 1
                        if frame_number % 100 == 0:
                            print(f"Processing buffer frame {i+1}/{buffer_frames} (total: {frame_number}/{new_frame_count})")
                        
                        # Continue word animation in buffer frames
                        word_frame_count += 1
                        if word_frame_count > frames_per_word:
                            word_frame_count = 1
                            current_word_index += 1
                            if current_word_index >= len(words):
                                current_word_index = len(words) - 1  # Stay on last word
                            current_word = words[current_word_index]
                        
                        # Calculate alpha for buffer frames
                        alpha = 255  # Full opacity
                        if word_frame_count <= fade_frames:  # Fade in
                            alpha = int(255 * (word_frame_count / fade_frames))
                        elif word_frame_count > frames_per_word - fade_frames:  # Fade out
                            alpha = int(255 * ((frames_per_word - word_frame_count) / fade_frames))
                        
                        # Ensure alpha is within bounds
                        alpha = max(0, min(255, alpha))
                        
                        # Create a sample image to measure current word dimensions
                        sample_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                        sample_draw = ImageDraw.Draw(sample_img)
                        text_bbox = sample_draw.textbbox((0, 0), current_word, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        
                        # Center the text both horizontally and vertically
                        text_x = (width - text_width) // 2
                        text_y = (height - text_height) // 2
                        
                        # Convert OpenCV BGR to RGB for Pillow
                        rgb_frame = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)
                        
                        # Create a Pillow Image from the frame
                        pil_image = Image.fromarray(rgb_frame)
                        
                        # Create a transparent overlay for the background
                        overlay = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))
                        overlay_draw = ImageDraw.Draw(overlay)
                        
                        # Add semi-transparent background for better readability
                        background_padding = 10
                        background_x1 = text_x - background_padding
                        background_y1 = text_y - background_padding
                        background_x2 = text_x + text_width + background_padding
                        background_y2 = text_y + text_height + background_padding
                        
                        # Draw semi-transparent background with fade effect
                        background_alpha = min(128, alpha // 2)
                        overlay_draw.rectangle(
                            [background_x1, background_y1, background_x2, background_y2],
                            fill=(0, 0, 0, background_alpha)
                        )
                        
                        # Convert PIL image to RGBA if it's not already
                        if pil_image.mode != 'RGBA':
                            pil_image = pil_image.convert('RGBA')
                            
                        # Composite the overlay onto the image
                        pil_image = Image.alpha_composite(pil_image, overlay)
                        
                        # Draw text with stroke and adjusted opacity
                        draw = ImageDraw.Draw(pil_image)
                        text_color_with_alpha = text_color + (alpha,)
                        stroke_color_with_alpha = stroke_color + (alpha,)
                        
                        draw.text(
                            (text_x, text_y),
                            current_word,
                            font=font,
                            fill=text_color_with_alpha,
                            stroke_width=config.CAPTION_STROKE_WIDTH,
                            stroke_fill=stroke_color_with_alpha
                        )
                        
                        # Convert back to OpenCV format
                        cv_frame = cv2.cvtColor(np.array(pil_image.convert('RGB')), cv2.COLOR_RGB2BGR)
                        
                        # Write the buffer frame to the output video
                        out.write(cv_frame)
        else:
            # Original implementation for displaying the entire caption text
            # Create a sample image to measure text dimensions
            sample_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            sample_draw = ImageDraw.Draw(sample_img)
            text_bbox = sample_draw.textbbox((0, 0), caption_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Center the text both horizontally and vertically
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2
            
            # Process each frame
            frame_number = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                frame_number += 1
                if frame_number % 100 == 0 or frame_number == 1:
                    print(f"Processing frame {frame_number}/{frame_count}")
                
                # Convert OpenCV BGR to RGB for Pillow
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Create a Pillow Image from the frame
                pil_image = Image.fromarray(rgb_frame)
                
                # Create a transparent overlay for the background
                overlay = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                
                # Add semi-transparent background for better readability
                background_padding = 10
                background_x1 = text_x - background_padding
                background_y1 = text_y - background_padding
                background_x2 = text_x + text_width + background_padding
                background_y2 = text_y + text_height + background_padding
                
                # Draw semi-transparent background
                overlay_draw.rectangle(
                    [background_x1, background_y1, background_x2, background_y2],
                    fill=(0, 0, 0, 128)  # Black with 50% opacity
                )
                
                # Convert PIL image to RGBA if it's not already
                if pil_image.mode != 'RGBA':
                    pil_image = pil_image.convert('RGBA')
                    
                # Composite the overlay onto the image
                pil_image = Image.alpha_composite(pil_image, overlay)
                
                # Draw text with stroke (outline)
                draw = ImageDraw.Draw(pil_image)
                draw.text(
                    (text_x, text_y),
                    caption_text,
                    font=font,
                    fill=text_color,
                    stroke_width=config.CAPTION_STROKE_WIDTH,
                    stroke_fill=stroke_color
                )
                
                # Convert back to OpenCV format (RGB to BGR)
                cv_frame = cv2.cvtColor(np.array(pil_image.convert('RGB')), cv2.COLOR_RGB2BGR)
                
                # Write the frame to the output video
                out.write(cv_frame)
        
        # Release resources
        cap.release()
        out.release()
        
        print(f"Caption added to video. Output saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error adding caption to video: {e}")
        return None

def add_audio_to_video(video_path: str, audio_path: str, output_path: str = None) -> Optional[str]:
    """
    Add audio to a video, replacing the original audio.
    This function uses FFmpeg via subprocess since OpenCV doesn't support audio.
    
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
        import subprocess
        import shutil
        
        # DEBUG: Print PATH environment variable
        print("\nDEBUG: Checking PATH environment variable:")
        path_env = os.environ.get('PATH', '')
        for path_item in path_env.split(os.pathsep):
            print(f"PATH entry: {path_item}")
            
            # Check if ffmpeg.exe exists in this directory
            potential_ffmpeg = os.path.join(path_item, 'ffmpeg.exe')
            if os.path.exists(potential_ffmpeg):
                print(f"Found ffmpeg.exe at: {potential_ffmpeg}")
            
            # Also check for ffmpeg without extension
            potential_ffmpeg_no_ext = os.path.join(path_item, 'ffmpeg')
            if os.path.exists(potential_ffmpeg_no_ext):
                print(f"Found ffmpeg at: {potential_ffmpeg_no_ext}")
        
        # First try to use the path from config if specified
        ffmpeg_path = config.FFMPEG_PATH if hasattr(config, 'FFMPEG_PATH') and config.FFMPEG_PATH else None
        
        if ffmpeg_path:
            print(f"Using FFmpeg path from config: {ffmpeg_path}")
            if not os.path.exists(ffmpeg_path):
                print(f"Warning: FFmpeg path specified in config ({ffmpeg_path}) does not exist.")
                ffmpeg_path = None
        
        # If no path in config or path doesn't exist, try to find in PATH
        if not ffmpeg_path:
            # Check if FFmpeg is installed and in PATH
            ffmpeg_path = shutil.which('ffmpeg')
            print(f"DEBUG: shutil.which('ffmpeg') returned: {ffmpeg_path}")
            
            # Also try with .exe extension explicitly (for Windows)
            ffmpeg_exe_path = shutil.which('ffmpeg.exe')
            print(f"DEBUG: shutil.which('ffmpeg.exe') returned: {ffmpeg_exe_path}")
            
            # Use ffmpeg.exe if found
            if ffmpeg_exe_path:
                ffmpeg_path = ffmpeg_exe_path
                print(f"Using ffmpeg.exe from PATH: {ffmpeg_path}")
        
        # If still not found, try common Windows locations
        if not ffmpeg_path:
            # Try to find ffmpeg in some common locations on Windows
            windows_common_ffmpeg_paths = [
                "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
                "C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe",
                "C:\\ffmpeg\\bin\\ffmpeg.exe",
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'ffmpeg', 'bin', 'ffmpeg.exe'),
                os.path.join(os.environ.get('APPDATA', ''), 'ffmpeg', 'bin', 'ffmpeg.exe')
            ]
            
            for path in windows_common_ffmpeg_paths:
                if os.path.exists(path):
                    print(f"Found ffmpeg at common Windows path: {path}")
                    ffmpeg_path = path
                    print(f"Using found ffmpeg at: {ffmpeg_path}")
                    break
        
        if not ffmpeg_path:
            print("Error: FFmpeg is not installed or not in your PATH.")
            print("Please install FFmpeg and make sure it's in your system PATH.")
            print("You can download FFmpeg from https://ffmpeg.org/download.html")
            print("Alternatively, set the FFMPEG_PATH in config.py to the full path of ffmpeg.exe")
            print("For now, returning the captioned video without audio.")
            return video_path  # Return the input video path since we can't add audio
        
        # Get video duration
        cap = cv2.VideoCapture(video_path)
        video_duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
        cap.release()
        
        # Command to add audio to video
        cmd = [
            ffmpeg_path,  # Use the full path to ffmpeg
            '-y',  # Overwrite output file if it exists
            '-i', video_path,  # Input video
            '-i', audio_path,  # Input audio
            '-c:v', 'copy',  # Copy video codec
            '-c:a', 'aac',  # Use AAC for audio
            '-map', '0:v:0',  # Use first video stream from first input
            '-map', '1:a:0',  # Use first audio stream from second input
            '-shortest',  # Finish encoding when the shortest input stream ends
            output_path
        ]
        
        # Run FFmpeg command
        print(f"Running FFmpeg to add audio to video...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error adding audio to video: {result.stderr}")
            print("Keeping the captioned video without audio.")
            return video_path  # Return the input video path on error
        
        print(f"Audio added to video. Output saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error adding audio to video: {e}")
        print("Keeping the captioned video without audio.")
        return video_path  # Return the input video path on exception

def process_video(video_path: str, caption_text: str, audio_path: str, output_path: str = None, word_by_word: bool = True) -> Optional[str]:
    """
    Process a video by adding both caption and audio.
    
    Args:
        video_path: Path to the input video file
        caption_text: Text to display as caption
        audio_path: Path to the audio file to add
        output_path: Path to save the final output video (if None, a default path will be created)
        word_by_word: If True, display one word at a time with animation
        
    Returns:
        Path to the output video or None if processing fails
    """
    # If no output path is specified, create one in the output directory
    if not output_path:
        video_name = os.path.basename(video_path)
        name, ext = os.path.splitext(video_name)
        output_path = os.path.join(config.OUTPUT_VIDEOS_DIR, f"{name}_processed{ext}")
    
    try:
        # Get audio duration for timing the captions correctly
        audio_duration = None
        if os.path.exists(audio_path):
            try:
                import subprocess
                import json
                import shutil
                
                # First try to use the path from config if specified
                ffprobe_path = config.FFPROBE_PATH if hasattr(config, 'FFPROBE_PATH') and config.FFPROBE_PATH else None
                
                if ffprobe_path:
                    print(f"Using FFprobe path from config: {ffprobe_path}")
                    if not os.path.exists(ffprobe_path):
                        print(f"Warning: FFprobe path specified in config ({ffprobe_path}) does not exist.")
                        ffprobe_path = None
                
                # If no path in config or path doesn't exist, try to find in PATH
                if not ffprobe_path:
                    # Check if FFprobe is installed and in PATH
                    ffprobe_path = shutil.which('ffprobe')
                    print(f"DEBUG: shutil.which('ffprobe') returned: {ffprobe_path}")
                    
                    # Also try with .exe extension explicitly (for Windows)
                    ffprobe_exe_path = shutil.which('ffprobe.exe')
                    print(f"DEBUG: shutil.which('ffprobe.exe') returned: {ffprobe_exe_path}")
                    
                    # Use ffprobe.exe if found
                    if ffprobe_exe_path:
                        ffprobe_path = ffprobe_exe_path
                
                # If FFmpeg exists in a custom path, check if FFprobe might be in the same directory
                if not ffprobe_path and hasattr(config, 'FFMPEG_PATH') and config.FFMPEG_PATH:
                    ffmpeg_dir = os.path.dirname(config.FFMPEG_PATH)
                    potential_ffprobe = os.path.join(ffmpeg_dir, 'ffprobe.exe')
                    if os.path.exists(potential_ffprobe):
                        ffprobe_path = potential_ffprobe
                        print(f"Found ffprobe.exe in the same directory as ffmpeg: {ffprobe_path}")
                
                if ffprobe_path:
                    # Command to get audio duration
                    cmd = [
                        ffprobe_path,
                        '-v', 'error',
                        '-show_entries', 'format=duration',
                        '-of', 'json',
                        audio_path
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        data = json.loads(result.stdout)
                        audio_duration = float(data['format']['duration'])
                        print(f"Audio duration: {audio_duration:.2f} seconds")
                    else:
                        print(f"Warning: Could not determine audio duration: {result.stderr}")
                else:
                    print("Warning: FFprobe not found, cannot determine audio duration")
            except Exception as e:
                print(f"Warning: Error determining audio duration: {e}")
                audio_duration = None
        
        # First add caption to the video with the audio duration for proper timing
        captioned_video = add_caption_to_video(
            video_path, 
            caption_text, 
            word_by_word=word_by_word,
            audio_duration=audio_duration
        )
        
        if not captioned_video:
            return None
        
        # Then add audio to the captioned video
        final_video = add_audio_to_video(captioned_video, audio_path, output_path)
        
        # Only remove the intermediate file if audio was successfully added
        # and the final video path is different from the captioned video path
        if final_video and final_video != captioned_video and os.path.exists(captioned_video) and captioned_video != video_path:
            os.remove(captioned_video)
            print(f"Removed intermediate file: {captioned_video}")
        elif not final_video or final_video == captioned_video:
            print(f"Keeping captioned video at: {captioned_video}")
        
        return final_video if final_video else captioned_video
        
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
    
    # List available fonts
    print("\nSearching for available fonts...")
    font_path = find_system_font(config.CAPTION_FONT)
    if font_path:
        print(f"Found font: {font_path}")
    else:
        print(f"Could not find font: {config.CAPTION_FONT}")
        print("Will use default font instead.")