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
from urllib.parse import urljoin

# Constants
APOD_URL = "https://science.nasa.gov/apod"
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
    explanation = next(
        (
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if "Explanation:" in p.get_text()
        ),
        None,
    )

    # The current NASA APOD page links its featured image through an APOD article.
    apod_link = next(
        (
            link
            for link in soup.find_all("a", href=re.compile(r"/image-article/apod-"))
            if link.find("img", src=True)
        ),
        None,
    )
    if apod_link:
        img_tag = apod_link.find("img")
        img_src = img_tag.get("src") if img_tag else None
        if isinstance(img_src, str):
            return {
                "img_url": urljoin(response.url, img_src),
                "explanation": explanation,
            }

    # Support the original APOD page, where the image is linked directly.
    image_link = soup.find(
        "a", href=re.compile(r"image/.*\.(jpg|jpeg|png|gif)$", re.IGNORECASE)
    )
    image_href = image_link.get("href") if image_link else None
    if image_link and image_link.find("img") and isinstance(image_href, str):
        return {
            "img_url": urljoin(response.url, image_href),
            "explanation": explanation,
        }

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
