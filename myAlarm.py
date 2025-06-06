#myAlarm.py
# run with pythonw, for best usage
# allows u to set your own alarm, using your own .mp3
# should run a separate gui, independant of the cmd prompt
# also should be low computer usage
# 'Set alarm' creates alarms if date/time is formatted right
# 'Clear alarm' cancels all active alarms
# Close the program by closing the gui
#_________________________________________________________

import time
import datetime
import pygame
import tkinter as tk
import tkinter.messagebox  # Explicitly import messagebox
from threading import Thread

class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("300x200")

        tk.Label(root, text="Enter alarm date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        tk.Label(root, text="Enter alarm time (HH:MM):").pack()
        self.time_entry = tk.Entry(root)
        self.time_entry.pack()

        self.start_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.start_button.pack()

        self.cancel_button = tk.Button(root, text="Cancel Alarm", command=self.cancel_alarm, state=tk.DISABLED)
        self.cancel_button.pack()

        self.alarm_active = False

    def show_alert(self):
        """Plays sound and then displays the visual alarm message."""
        pygame.mixer.init()
        pygame.mixer.music.load("Fanfare.mp3")  # Ensure the file is in the same directory
        pygame.mixer.music.play()  # Start sound BEFORE showing message

        tkinter.messagebox.showinfo("Alarm!", "Time's up!")  # Message box appears after sound starts

    def check_alarm(self, alarm_time):
        """Checks system time and triggers the alarm."""
        while self.alarm_active:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            if current_time == alarm_time:
                self.show_alert()
                break
            time.sleep(10)  # Low CPU usage

    def set_alarm(self):
        """Starts the alarm countdown."""
        alarm_date = self.date_entry.get()
        alarm_hour = self.time_entry.get()
        alarm_time = f"{alarm_date} {alarm_hour}"

        self.alarm_active = True
        self.cancel_button.config(state=tk.NORMAL)

        Thread(target=self.check_alarm, args=(alarm_time,)).start()
        tk.Label(self.root, text=f"Alarm set for {alarm_time}").pack()

    def cancel_alarm(self):
        """Manually cancels the alarm before it goes off."""
        self.alarm_active = False
        pygame.mixer.music.stop()  # Stop alarm sound if playing
        self.cancel_button.config(state=tk.DISABLED)
        tkinter.messagebox.showinfo("Alarm Cancelled", "Alarm has been stopped.")

# Run GUI application without blocking terminal
if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
