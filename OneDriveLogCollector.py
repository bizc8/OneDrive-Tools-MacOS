# This python app collects the OneDrive logs, stores them in a zip file in the desktop and parses the SyncDiagnostics.log into a Window for easy review
# Application tested in MacOS 13.5.2

import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os
import zipfile
import re
from datetime import datetime
 
def collect_logs():
    cmd_path = "/Applications/OneDrive.app/Contents/Resources/CollectLogsStandalone.command"
   
    if not os.path.exists(cmd_path):
        messagebox.showerror("Error", f"Command file not found at {cmd_path}")
        return
   
    try:
        subprocess.run(['open', cmd_path])
        messagebox.showinfo("Success", "Logs are being collected! Please wait for them to be extracted.")
        retrieve_and_parse_logs()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run the command. Error: {e}")
 
def retrieve_and_parse_logs():
    # Folder path where the logs are saved
    desktop_path = os.path.expanduser("~/Desktop")
 
    # Regex pattern to match filenames that start with OneDriveLogs and contain a date and time
    pattern = re.compile(r'^OneDriveLogs_(\d{8}_\d{4})\.zip$')
   
    # List all matching files on the desktop
    matching_files = [f for f in os.listdir(desktop_path) if pattern.match(f)]
 
    # If no matching files found, exit
    if not matching_files:
        messagebox.showerror("Error", "No log files found on the desktop.")
        return
   
    # Sort the files based on date and time and get the most recent one
    latest_file = sorted(matching_files, key=lambda x: pattern.match(x).group(1), reverse=True)[0]
 
    zip_path = os.path.join(desktop_path, latest_file)
   
    # Extracting the zip file
    extract_folder = "/tmp/onedrive_logs"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
 
    # Parsing the log file
    username = os.path.basename(os.path.expanduser("~"))  # get the logged-in username
    log_path = os.path.join(extract_folder, f"Users/{username}/Library/Logs/OneDrive/Business1/SyncDiagnostics.log")
   
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            log_contents = f.read()
            text_widget.insert(tk.END, log_contents)
    else:
        messagebox.showerror("Error", "Could not find the log file in the extracted contents.")
 
app = tk.Tk()
app.title("OneDrive Log Collector")
 
btn_collect_logs = tk.Button(app, text="Collect Logs", command=collect_logs)
btn_collect_logs.pack(pady=20)
 
# Adding a widget to display the log file content
text_widget = scrolledtext.ScrolledText(app, width=100, height=300)
text_widget.pack(pady=20)
 
app.mainloop()
