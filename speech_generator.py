"""
Text-to-speech module for the Video Modification Bot.
Handles converting generated text to speech using Google Text-to-Speech (gTTS).
"""

import os
from gtts import gTTS
from typing import Optional
import config

def text_to_speech(text: str, output_file: str = None, 
                   language: str = config.TTS_LANGUAGE, 
                   slow: bool = config.TTS_SLOW) -> Optional[str]:
    """
    Convert text to speech using Google Text-to-Speech.
    
    Args:
        text: The text to convert to speech
        output_file: Path to save the audio file (if None, a temporary file will be created)
        language: Language code for the speech
        slow: Whether to speak slowly
        
    Returns:
        Path to the generated audio file or None if conversion fails
    """
    if not text:
        print("Error: No text provided for text-to-speech conversion.")
        return None
    
    # If no output file is specified, create one in the output directory
    if not output_file:
        # Create a filename based on the first few words of the text
        words = text.split()[:3]
        filename = "_".join(words).lower()
        filename = "".join(c if c.isalnum() or c == "_" else "" for c in filename)
        output_file = os.path.join(config.OUTPUT_VIDEOS_DIR, f"{filename}_audio.mp3")
    
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=slow)
        
        # Save the audio file
        tts.save(output_file)
        
        print(f"Speech generated and saved to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

# For testing
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs(config.OUTPUT_VIDEOS_DIR, exist_ok=True)
    
    # Test with a sample text
    sample_text = "Life is about making an impact, not making an income. Whatever the mind can conceive and believe, it can achieve."
    audio_file = text_to_speech(sample_text)
    
    if audio_file:
        print(f"Successfully generated speech: {audio_file}")
    else:
        print("Failed to generate speech.")
