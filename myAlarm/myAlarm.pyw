# myAlarm.py
# run with pythonw, for best usage
# allows you to set your own alarm, using your own .mp3
# runs a separate GUI, independent of the cmd prompt
# low computer usage
# 'Set alarm' creates alarms if date/time is formatted right
# 'Clear alarm' cancels all active alarms
# Close the program by closing the GUI
#_________________________________________________________

import time
import datetime
import winsound
import tkinter as tk
import tkinter.messagebox
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
        winsound.PlaySound("Fanfare.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        tkinter.messagebox.showinfo("Alarm!", "Time's up!")

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

        Thread(target=self.check_alarm, args=(alarm_time,), daemon=True).start()
        tk.Label(self.root, text=f"Alarm set for {alarm_time}").pack()

    def cancel_alarm(self):
        """Manually cancels the alarm before it goes off."""
        self.alarm_active = False
        winsound.PlaySound(None, winsound.SND_PURGE)  # Stop playback
        self.cancel_button.config(state=tk.DISABLED)
        tkinter.messagebox.showinfo("Alarm Cancelled", "Alarm has been stopped.")

# Run GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
