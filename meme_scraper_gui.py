import os
import requests
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext

# SETTINGS
subreddit = "memes"
limit = 10  # Pull extra for better odds
after_file = "after_token.txt"  # Pagination token file

# Define Downloads base path
base_folder = os.path.join(os.path.expanduser("~"), "Downloads")

# Faces list
faces = [
    """
   -----
 /       \\
|  o   o  |
|    ^    |
|  \\___/  |
 \\_______/
""",
    """
   -----
 /       \\
| -o- -o- |
|    ^    |
|   ---   |
 \\_______/
""",
    """
   -----
 /  ^ ^  \\
|  o   o  |
|    ~    |
|   \\_/   |
 \\_______/
""",
    """
   -----
 / >   < \\
|  o   o  |
|    -    |
|  _____  |
 \\_______/
""",
    """
   -----
 /       \\
|  0   0  |
|    -    |
|   \\_/   |
 \\_______/
"""
]

# Function to download memes
def download_memes():
    status_text.delete('1.0', tk.END)

    # Find unique folder name
    folder_name = "Memes"
    full_path = os.path.join(base_folder, folder_name)
    counter = 1
    while os.path.exists(full_path):
        full_path = os.path.join(base_folder, f"{folder_name}{counter}")
        counter += 1

    os.makedirs(full_path)
    status_text.insert(tk.END, f"Saving memes into: {full_path}\n")

    # Read 'after' token if exists
    if os.path.exists(after_file):
        with open(after_file, "r") as f:
            after = f.read().strip()
    else:
        after = ""

    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    if after:
        url += f"&after={after}"

    headers = {"User-Agent": "MemeScraperBot/1.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]
        memes = data["children"]
        after = data.get("after")

        # Save new 'after' token
        if after:
            with open(after_file, "w") as f:
                f.write(after)
        else:
            if os.path.exists(after_file):
                os.remove(after_file)

        download_count = 0
        for meme in memes:
            image_url = meme["data"].get("url_overridden_by_dest")

            if image_url and (image_url.endswith(".jpg") or image_url.endswith(".png") or image_url.endswith(".jpeg")):
                try:
                    image_data = requests.get(image_url).content
                    filename = os.path.join(full_path, f"meme_{download_count + 1}.jpg")
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    status_text.insert(tk.END, f"[+] Downloaded: meme_{download_count + 1}.jpg\n")
                    download_count += 1
                except:
                    status_text.insert(tk.END, f"[-] Failed to download one image.\n")

            if download_count >= 5:
                break

        if download_count == 0:
            status_text.insert(tk.END, "[-] No image memes found this time. Try again.\n")
    else:
        status_text.insert(tk.END, f"[-] Failed to fetch memes. Status: {response.status_code}\n")

    # Pick random face and show it
    chosen_face = random.choice(faces)
    status_text.insert(tk.END, "\n" + chosen_face + "\n")
    status_text.insert(tk.END, "---------- ENJOY YOUR MEMES! ----------\n")

# Setup GUI
root = tk.Tk()
root.title("Meme Scraper GUI")
root.geometry("500x650")
root.resizable(False, False)

# COLORS
root.configure(bg="blue")

# Title
title_label = tk.Label(root, text="Meme Scraper GUI", font=("Arial", 18, "bold"), bg="blue", fg="white")
title_label.pack(pady=(10, 0))

# Created by Joseph Morrison
creator_label = tk.Label(root, text="Created by Joseph Morrison", font=("Arial", 10), bg="blue", fg="black")
creator_label.pack(pady=(0, 10))

# Download Button
download_button = tk.Button(root, text="Download Memes", font=("Arial", 14), command=download_memes, bg="red", fg="white", activebackground="darkred", activeforeground="white")
download_button.pack(pady=10)

# Status Text
status_text = scrolledtext.ScrolledText(root, width=60, height=25, font=("Courier", 10), bg="blue", fg="white", insertbackground="white")
status_text.pack(padx=10, pady=10)

# Bottom Info (Version and License)
bottom_frame = tk.Frame(root, bg="blue")
bottom_frame.pack(pady=(10,5))

version_label = tk.Label(bottom_frame, text="Version v1.1.0", font=("Arial", 9), bg="blue", fg="black")
version_label.pack()

license_label = tk.Label(bottom_frame, text="CC BY-NC-ND 4.0", font=("Arial", 9), bg="blue", fg="black")
license_label.pack()

root.mainloop()

