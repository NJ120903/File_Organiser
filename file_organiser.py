import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

file_types = {
    'Images': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
    'Documents': ['txt', 'doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx'],
    'Videos': ['mp4', 'avi', 'mov', 'mkv'],
    'Music': ['mp3', 'wav', 'flac', 'aac'],
    'Archives': ['zip', 'rar', '7z', 'tar', 'gz'],
    'Executables': ['exe', 'msi', 'bat'],
    'Programming': ['py', 'java', 'c', 'cpp', 'h', 'html', 'css', 'js'],
    'Others': []
}

def organize_files(directory, root_window):
    progress_var.set(0)
    total_files = sum(len(files) for _, _, files in os.walk(directory))

    for dir_path, _, files in os.walk(directory):
        for file in files:
            src_path = os.path.join(dir_path, file)
            file_ext = file.split('.')[-1].lower()
            category = 'Others'  # Default category

            if not file_ext or file_ext in ('', ' '):
                # Treat files without recognized extensions as "others"
                pass
            else:
                for cat, extensions in file_types.items():
                    if file_ext in extensions:
                        category = cat
                        break

            dest_folder = os.path.join(directory, category)
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, file)
            shutil.move(src_path, dest_path)

            progress_var.set(progress_var.get() + 1)
            progress_label.config(text=f'Progress: {progress_var.get()} / {total_files}')
            root_window.update()

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def organize():
    directory = directory_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory path")
        return

    organize_files(directory, root)
    messagebox.showinfo("Success", "Files organized successfully")

root = tk.Tk()
root.title("File Organizer")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

directory_label = ttk.Label(frame, text="Select Directory:")
directory_label.grid(row=0, column=0, sticky=tk.W)

directory_entry = ttk.Entry(frame, width=50)
directory_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = ttk.Button(frame, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=2, padx=5, pady=5)

organize_button = ttk.Button(frame, text="Organize", command=organize)
organize_button.grid(row=1, column=1, pady=10)

progress_var = tk.IntVar()
progress_label = ttk.Label(frame, text="Progress: 0 / 0")
progress_label.grid(row=2, column=1, pady=5)

root.mainloop()
