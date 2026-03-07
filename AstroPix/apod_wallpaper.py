#apod_wallpaper.py - Download today's APOD image and set it as wallpaper on Windows 11

# Check if running in the correct venv
import sys
import os
def prompt_close_terminal():
    user_input = input("Do you want to close the terminal? (y/n): ").strip().lower()
    if user_input == "y":
        sys.exit(0)
    else:
        print("Terminal will remain open.")
        return

expected_venv = os.path.normpath(r"C:/Users/Dwash/OneDrive - BCIT/Documents/Mikhail/School/BCIT ECET/Notes/7/other/py/AstroPix/.venv")
actual_prefix = os.path.normpath(sys.prefix)
if not actual_prefix.startswith(expected_venv):
    print("\nWARNING: You are not running this script in the required virtual environment.")
    print("To use this program, run it with the virtual environment where dependencies are installed.")
    print("Example command:")
    print("  & 'c:/Users/Dwash/OneDrive - BCIT/Documents/Mikhail/School/BCIT ECET/Notes/7/other/py/AstroPix/.venv/Scripts/python.exe' apod_wallpaper.py")
    print("Or search for the Startup folder shortcut that launches this app automatically.")
    prompt_close_terminal()
import os
import re
import requests
from bs4 import BeautifulSoup
import ctypes
import shutil

# Constants
APOD_URL = "https://apod.nasa.gov/apod/astropix.html"
DOWNLOADS_DIR = os.path.expanduser(r"C:/Users/Dwash/Downloads")

def prompt_close_terminal():
    user_input = input("Do you want to close the terminal? (y/n): ").strip().lower()
    if user_input == "y":
        import sys
        sys.exit(0)
    else:
        print("Terminal will remain open.")
        return

def get_apod_image_url():
    response = requests.get(APOD_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # Try to find image inside <a> tag first (common for APOD)
    a_tag = soup.find("a", href=re.compile(r"image/.*\\.(jpg|jpeg|png|gif)$", re.IGNORECASE))
    if a_tag and a_tag.find("img"):
        img_src = a_tag["href"]
        if not img_src.startswith("http"):
            img_src = "https://apod.nasa.gov/apod/" + img_src
        # Find explanation (usually in <p> tags near the image)
        explanation = None
        # Try to find the <p> tag after the image's parent <center> tag
        center_tag = a_tag.find_parent("center")
        if center_tag:
            # Explanation is often the next <p> after <center>
            next_p = center_tag.find_next_sibling("p")
            if next_p:
                explanation = next_p.get_text(strip=True)
        # Fallback: find all <p> tags and pick the one with 'Explanation:'
        if not explanation:
            for p in soup.find_all("p"):
                if "Explanation:" in p.get_text():
                    explanation = p.get_text(strip=True)
                    break
        return {"img_url": img_src, "explanation": explanation}
    # Fallback: find first <img> tag
    img_tag = soup.find("img")
    if img_tag and "src" in img_tag.attrs:
        img_src = img_tag["src"]
        if not img_src.startswith("http"):
            img_src = "https://apod.nasa.gov/apod/" + img_src
        # Try to find explanation as above
        explanation = None
        center_tag = img_tag.find_parent("center")
        if center_tag:
            next_p = center_tag.find_next_sibling("p")
            if next_p:
                explanation = next_p.get_text(strip=True)
        if not explanation:
            for p in soup.find_all("p"):
                if "Explanation:" in p.get_text():
                    explanation = p.get_text(strip=True)
                    break
        return {"img_url": img_src, "explanation": explanation}
    # Check for video link
    video_tag = soup.find("a", string=re.compile(r"video|youtube|vimeo|facebook", re.IGNORECASE))
    if video_tag and video_tag.has_attr("href"):
        return {"video": video_tag["href"]}
    raise Exception("No image or video found on APOD page.")


def download_image(img_url, download_dir):
    filename = "apod_wallpaper.jpg"
    file_path = os.path.join(download_dir, filename)
    # Delete previous image with the same name
    if os.path.exists(file_path):
        os.remove(file_path)
    # Download new image
    response = requests.get(img_url, stream=True)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    return file_path


def set_wallpaper(image_path):
    # Set wallpaper for all screens (Windows 11)
    SPI_SETDESKWALLPAPER = 20
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, 3
    )
    if not result:
        raise Exception("Failed to set wallpaper.")


def main():
    try:
        result = get_apod_image_url()
        if isinstance(result, dict) and "video" in result:
            print("Today's APOD is a video.")
            print(f"Video link: {result['video']}")
            user_input = input("Do you want to close the terminal? (y/n): ").strip().lower()
            if user_input == "y":
                import sys
                sys.exit(0)
            else:
                print("Terminal will remain open.")
                return
        # result is a dict with 'img_url' and 'explanation'
        img_url = result["img_url"]
        explanation = result.get("explanation")
        print(f"Image URL: {img_url}")
        image_path = download_image(img_url, DOWNLOADS_DIR)
        print(f"Downloaded to: {image_path}")
        set_wallpaper(image_path)
        print("Wallpaper set successfully.")
        if explanation:
            print("\nAPOD Explanation:")
            print(explanation)
        else:
            print("\nNo explanation found on the APOD page.")
        prompt_close_terminal()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError as e:
        if e.name == "bs4":
            print("\nERROR: BeautifulSoup (bs4) is not installed in your current Python environment.")
            print("To use this program, run it with the virtual environment where dependencies are installed.")
            print("Example command:")
            print("  & 'c:/Users/Dwash/OneDrive - BCIT/Documents/Mikhail/School/BCIT ECET/Notes/7/other/py/AstroPix/.venv/Scripts/python.exe' apod_wallpaper.py")
            print("Or search for the Startup folder shortcut that launches this app automatically.")
            prompt_close_terminal()
        else:
            print(f"ModuleNotFoundError: {e}")
            prompt_close_terminal()
