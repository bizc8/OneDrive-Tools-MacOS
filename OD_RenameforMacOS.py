import os
import getpass
import tkinter as tk
from tkinter import messagebox
import glob

def replace_invalid_characters(directory):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']  # Define the invalid characters to replace
    rename_count = 0  # Counter to keep track of renamed files

    for root, dirs, files in os.walk(directory):
        for filename in files:
            new_filename = filename
            for char in invalid_chars:
                new_filename = new_filename.replace(char, '_')  # Replace invalid characters with underscores (_)
            if new_filename != filename:
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)
                
                # Prompt user to confirm file rename
                response = messagebox.askyesno("Rename Confirmation", f"The following file has been found:\n\n{filename}\n\nIt will be renamed to:\n\n{new_filename}\n\nContinue?")
                if response:
                    os.rename(old_path, new_path)
                    rename_count += 1

    short_directory = os.path.basename(directory)  # Get the short directory name
    messagebox.showinfo("Rename Summary", f"{rename_count} file(s) renamed in directory:\n\n{short_directory}")

# Get the username of the currently logged-on user
username = getpass.getuser()

# Specify the base directory path
base_directory = f"/Users/{username}"

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Search for directories that begin with "/Users/{username}/OneDrive"
matching_directories = glob.glob(f"{base_directory}/OneDrive*")

# Prompt user to start the renaming process
response = messagebox.askokcancel("Rename Files", "This process will rename files in your OneDrive directories with invalid characters.\n\nDo you want to continue?")
if response:
    # Iterate through the matching directories and call the function to replace invalid characters in file names
    for directory in matching_directories:
        replace_invalid_characters(directory.replace('*', r'\*'))
else:
    messagebox.showinfo("Operation Canceled", "Rename operation canceled by user.")
