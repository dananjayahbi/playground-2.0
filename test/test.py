import tkinter as tk
import re
import pyperclip

# List to store extracted image URLs
image_urls = []

# Function to extract image URL from input
def extract_image_url(input_text):
    match = re.search(r'\[img\](.*?)\[/img\]', input_text)
    if match:
        return match.group(1)
    return None

# Function to handle input and update the list
def process_input():
    input_text = url_entry.get("1.0", tk.END).strip()
    if not input_text:
        return
    
    # Extract the image URL
    extracted_url = extract_image_url(input_text)
    if extracted_url:
        if extracted_url not in image_urls:  # Avoid duplicates
            image_urls.append(extracted_url)
            update_display()
            url_entry.delete("1.0", tk.END)  # Clear input field
    else:
        return  # Ignore invalid inputs

# Function to update the display with numbered URLs
def update_display():
    for widget in url_frame.winfo_children():
        widget.destroy()  # Clear previous widgets
    
    for i, img_url in enumerate(image_urls, start=1):
        url_text = f"{i}. {img_url}"  # Numbered list format
        url_label = tk.Label(url_frame, text=url_text, fg="blue", cursor="hand2", wraplength=400, anchor="w", justify="left")
        url_label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        
        copy_button = tk.Button(url_frame, text="Copy", command=lambda u=img_url: copy_to_clipboard(u))
        copy_button.grid(row=i, column=1, padx=5, pady=2)

# Function to copy URL to clipboard
def copy_to_clipboard(url):
    pyperclip.copy(url)  # No popup message

# Function to clear everything
def clear_all():
    global image_urls
    image_urls = []  # Reset list
    url_entry.delete("1.0", tk.END)  # Clear input field
    update_display()  # Refresh UI

# GUI Setup
root = tk.Tk()
root.title("Flickr Image URL Extractor")
root.geometry("550x500")

# Input field (Fixed text retrieval issue)
url_entry = tk.Text(root, height=3, width=60)  # Multiline input
url_entry.pack(pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()

add_button = tk.Button(button_frame, text="Extract & Add", command=process_input)
add_button.pack(side="left", padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_all)
clear_button.pack(side="left", padx=5)

# Scrollable Frame for displaying extracted URLs
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
url_frame = tk.Frame(canvas)

url_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=url_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Start the Tkinter loop
root.mainloop()
