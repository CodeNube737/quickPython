###############################################################################################
# Author: Mikhail R, with the help of OpenAI
# Date: 1/20/2025
# This script allows the user to work on their computer with some of their favourite pictures 
#	openning up every 5 minutes. Must have Pillow installed.

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to choose a directory using a file dialog
def choose_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory()  # Open the directory chooser dialog
    return directory

# Function to display an image in a new window
def display_image(image_path):
    window = tk.Toplevel()  # Create a new top-level window
    window.title("Image Viewer")  # Set the window title
    img = Image.open(image_path)  # Open the image file
    img = ImageTk.PhotoImage(img)  # Convert the image to a format tkinter can use
    panel = tk.Label(window, image=img)  # Create a label widget to display the image
    panel.image = img  # Keep a reference to the image to prevent garbage collection
    panel.pack(side="top", fill="both", expand="yes")  # Pack the label widget into the window

# Function to schedule the display of new images
def schedule_images(directory, image_files, index):
    image_path = os.path.join(directory, image_files[index])  # Get the path of the current image
    display_image(image_path)  # Display the image
    index = (index + 1) % len(image_files)  # Move to the next image, looping back to the start if necessary
    root.after(300000, schedule_images, directory, image_files, index)  # Schedule the next image display in 5 minutes

# Main function to run the program
def main():
    global root
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    directory = choose_directory()  # Ask the user to choose a directory
    if not directory:
        print("No directory chosen. Exiting.")
        return

    # Get a list of image files in the chosen directory
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    if not image_files:
        print("No images found in the directory. Exiting.")
        return

    index = 0
    schedule_images(directory, image_files, index)  # Start scheduling the image display

    print("Press 's' to stop the program.")  # Display the stop instruction
    while True:
        if input("Type 's' to stop: ").strip().lower() == 's':  # Check if the user wants to stop the program
            break

if __name__ == "__main__":
    main()  # Run the main function
