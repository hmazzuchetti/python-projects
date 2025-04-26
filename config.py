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

# Ollama API configuration
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://127.0.0.1:11434")
TEXT_MODEL = "deepseek-r1:1.5b"  # Using locally running deepseek model through Ollama

# Text generation settings
TEXT_PROMPT = "Generate a short, motivational, fun and philosophical quote or message that would work well as a video caption. Keep it under 150 characters."

# Text-to-speech settings
TTS_LANGUAGE = "en"  # English
TTS_SLOW = False  # Normal speed

# Caption settings
CAPTION_FONT = "Impact"  # Changed to Impact which is good for ticker-style text
CAPTION_FONTSIZE = 50  # Keeping the larger font size we just set
CAPTION_COLOR = "yellow"  # Changed from white to yellow for better visibility
CAPTION_STROKE_COLOR = "black"
CAPTION_STROKE_WIDTH = 2  # Increased stroke width for better contrast
CAPTION_POSITION = "bottom"  # Position at the bottom of the video
