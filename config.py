"""
Configuration file for the Video Modification Bot.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Directories
INPUT_VIDEOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input_videos")
OUTPUT_VIDEOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_videos")

# External tools paths
# Set these to the full path if they're not in your system PATH
FFMPEG_PATH = os.getenv("FFMPEG_PATH", None)  # Will use PATH if None
FFPROBE_PATH = os.getenv("FFPROBE_PATH", None)  # Will use PATH if None

# Ollama API configuration
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://127.0.0.1:11434")
TEXT_MODEL = "deepseek-r1:1.5b"  # Using locally running deepseek model through Ollama

# Text generation settings
TEXT_PROMPT = "Generate a short, motivational, fun and philosophical quote or message that would work well as a video caption. Keep it under 150 characters."

# Text-to-speech settings
TTS_LANGUAGE = "en"  # English
TTS_SLOW = False  # Normal speed

# Caption settings
CAPTION_FONT = "Impact"  # Any font name installed on your system
CAPTION_FONTSIZE = 50
CAPTION_COLOR = "yellow"  # or RGB tuple like (255, 255, 0)
CAPTION_STROKE_COLOR = "black"  # or RGB tuple like (0, 0, 0)
CAPTION_STROKE_WIDTH = 2
CAPTION_POSITION = "bottom"  # "top", "center", or "bottom"

