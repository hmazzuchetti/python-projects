"""
Setup MoviePy configuration to use ImageMagick.
Run this script once after installing ImageMagick.
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_moviepy():
    """Configure MoviePy to use ImageMagick."""
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
            
            # For MoviePy 2.1.2+, we'll set the environment variable
            os.environ["IMAGEMAGICK_BINARY"] = path
            
            # Also create a moviepy_config.txt file with the path
            config_path = Path.home() / ".moviepy" / "config_defaults.py"
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, "w") as f:
                f.write(f'IMAGEMAGICK_BINARY = r"{path}"\n')
            
            print("MoviePy configuration updated successfully!")
            return True
    
    # If we can't find it automatically, ask the user
    print("Could not find ImageMagick automatically.")
    print("Please enter the full path to the ImageMagick 'magick.exe' executable:")
    user_path = input("> ").strip('"')
    
    if os.path.exists(user_path):
        # For MoviePy 2.1.2+, we'll set the environment variable
        os.environ["IMAGEMAGICK_BINARY"] = user_path
        
        # Also create a moviepy_config.txt file with the path
        config_path = Path.home() / ".moviepy" / "config_defaults.py"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, "w") as f:
            f.write(f'IMAGEMAGICK_BINARY = r"{user_path}"\n')
            
        print("MoviePy configuration updated successfully!")
        return True
    else:
        print(f"Error: The path '{user_path}' does not exist.")
        print("Please make sure ImageMagick is installed correctly.")
        return False

def check_imagemagick_installation():
    """Check if ImageMagick is installed and available in PATH."""
    try:
        # Try to run the magick command to check if it's in PATH
        result = subprocess.run(["magick", "-version"], 
                             capture_output=True, 
                             text=True, 
                             check=False)
        if result.returncode == 0:
            print("ImageMagick is installed and available in PATH.")
            print(result.stdout.splitlines()[0])
            return True
    except FileNotFoundError:
        print("ImageMagick is not found in PATH.")
        
    # Also check common installation paths
    return setup_moviepy()

if __name__ == "__main__":
    print("Checking ImageMagick installation...")
    if check_imagemagick_installation():
        print("MoviePy configuration is ready.")
    else:
        print("Please install ImageMagick from https://imagemagick.org/script/download.php")
        print("Make sure to enable 'Add application directory to your system path' during installation.")