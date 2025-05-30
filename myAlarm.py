#myAlarm.py
######################################################################################

import time
import datetime
import pygame
import tkinter as tk
import tkinter.messagebox  # Explicitly import messagebox
from threading import Thread

def show_alert():
    """Displays a visual alarm message."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    tkinter.messagebox.showinfo("Alarm!", "Time's up!")  # Corrected messagebox call
    root.destroy()

def play_alarm_sound():
    """Plays alarm sound using pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load("Fanfare.mp3")  ################ Replace with a valid sound file
    pygame.mixer.music.play()

def set_alarm(alarm_time):
    """Checks system time and triggers the alarm."""
    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if current_time == alarm_time:
            Thread(target=show_alert).start()
            play_alarm_sound()
            break
        time.sleep(10)  # Low CPU usage

# User input
alarm_date = input("Enter alarm date (YYYY-MM-DD): ")
alarm_hour = input("Enter alarm time (HH:MM): ")
alarm_time = f"{alarm_date} {alarm_hour}"

# Start alarm
print(f"Alarm set for {alarm_time}")
set_alarm(alarm_time)
