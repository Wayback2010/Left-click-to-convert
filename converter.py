import sys
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from pydub import AudioSegment

def get_conversion_options(ext):
    image_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']
    audio_exts = ['.mp3', '.wav', '.flac', '.ogg']
    if ext in image_exts:
        return [e for e in image_exts if e != ext]
    elif ext in audio_exts:
        return [e for e in audio_exts if e != ext]
    else:
        return []

def convert_file(file_path, target_ext):
    ext = os.path.splitext(file_path)[1].lower()
    base = os.path.splitext(file_path)[0]
    new_path = base + target_ext

    try:
        if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
            img = Image.open(file_path)
            img.save(new_path)
        elif ext in ['.mp3', '.wav', '.flac', '.ogg']:
            audio = AudioSegment.from_file(file_path)
            audio.export(new_path, format=target_ext.replace('.', ''))
        else:
            messagebox.showerror("Error", "Unsupported file type")
            return
        messagebox.showinfo("Success", f"Converted to {new_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        root.destroy()

def launch_gui(file_path):
    global root
    ext = os.path.splitext(file_path)[1].lower()
    options = get_conversion_options(ext)

    if not options:
        messagebox.showerror("Error", "No conversion options available for this file type")
        return

    root = tk.Tk()
    root.title("Convert File")
    tk.Label(root, text=f"Convert {os.path.basename(file_path)} to:").pack(pady=10)

    for opt in options:
        btn = tk.Button(root, text=opt.upper(), width=20,
                        command=lambda o=opt: convert_file(file_path, o))
        btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        launch_gui(sys.argv[1])
    else:
        print("No file path provided")
