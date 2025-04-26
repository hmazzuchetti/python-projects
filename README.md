# Video Modification Bot - User Guide

## Overview
The Video Modification Bot is a Python application that automatically:
1. Selects a random video from your input folder
2. Generates a motivational, fun, and philosophical caption using AI
3. Converts the caption to speech with a mysterious voice
4. Adds both the caption and voice to the video
5. Saves the modified video to an output folder

## Requirements
- Python 3.6 or higher
- OpenAI API key (for text generation)
- Internet connection (for text-to-speech)

## Installation

### 1. Clone or download the project
Place the video_bot folder in your desired location.

### 2. Install dependencies
The bot requires several Python packages. They can be installed using pip:

```bash
pip install moviepy openai gtts python-dotenv requests numpy
```

### 3. Set up your OpenAI API key
Create a `.env` file in the project directory by copying the provided template:

```bash
cp .env.template .env
```

Then edit the `.env` file and replace `your_api_key_here` with your actual OpenAI API key.

## Usage

### 1. Add videos to the input folder
Place your video files in the `input_videos` directory. The bot supports common video formats:
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)
- FLV (.flv)

### 2. Run the bot
Navigate to the project directory and run:

```bash
python main.py
```

### 3. View the results
The processed video will be saved in the `output_videos` directory. The filename will include "processed" to distinguish it from the original.

## Customization

You can customize the bot's behavior by editing the `config.py` file:

- **Text Generation**: Modify the prompt or model used for generating captions
- **Text-to-Speech**: Change the language or speech speed
- **Caption Style**: Adjust font, size, color, and position

## Troubleshooting

### No videos found
Make sure you have placed video files in the `input_videos` directory.

### API key errors
Verify that your OpenAI API key is correctly set in the `.env` file.

### Video processing errors
Ensure your videos are in a supported format and not corrupted.

## Future Enhancements
This is a prototype version. Future enhancements could include:
- Multiple font styles and animations for captions
- Customizable voice characteristics
- Automatic scheduling
- Web interface for easier management

## Project Structure
- `main.py`: Main script that integrates all components
- `config.py`: Configuration settings
- `video_selector.py`: Handles random video selection
- `text_generator.py`: Generates caption text using OpenAI
- `speech_generator.py`: Converts text to speech
- `video_editor.py`: Adds captions and audio to videos
- `input_videos/`: Directory for input videos
- `output_videos/`: Directory for processed videos
