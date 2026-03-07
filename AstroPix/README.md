# AstroPix APOD Wallpaper

This script downloads NASA's Astronomy Picture of the Day (APOD) and sets it as your Windows 11 desktop wallpaper. It also prints the explanation from the APOD page.

## Features
- Downloads the daily APOD image
- Sets it as your Windows wallpaper
- Prints the APOD explanation
- Handles video APODs gracefully
- Checks for required Python virtual environment

## Requirements
- Python 3.x
- Packages: `requests`, `beautifulsoup4`
- Windows 11

## Setup
1. Clone this repository.
2. Create and activate a Python virtual environment (recommended):
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install requests beautifulsoup4
   ```

## Usage
Run the script from your virtual environment:
```sh
python apod_wallpaper.py
```
Or, use the full path to your venv's Python executable as shown in the script's warning message.

## Notes
- The script is designed for Windows 11 and may not work on other operating systems.
- The APOD explanation is printed after the wallpaper is set.
- If today's APOD is a video, the script will print the video link instead.

## License
This project is provided under the MIT License.
