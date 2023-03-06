import time
import tkinter as tk
from tkinter import filedialog
import threading
import subprocess
import os
import sys
import signal

SPOTDL_VERSION = os.environ.get("SPOTDL_VERSION")

try:
    os.chdir(sys._MEIPASS)
except:
    input("It seems like you are running this script from source. Please build the script with pyinstaller and run the executable. Press enter to exit.")
    exit()
exe_path = os.path.join(os.getcwd(), f"spotdl-{SPOTDL_VERSION}.exe" if os.name == "nt" else f"spotdl-{SPOTDL_VERSION}-linux")

bitrates = ["128k", "192k", "256k", "320k"]
download_path  = None
current_bitrate = bitrates[0]
download_thread = None
class ErrorHandler:
    def __init__(self):
        self.error = False
        self.error_message = ""
    
    def set_error(self, error_message):
        self.error = True
        self.error_message = error_message

class SpotDL:
    def __init__(self,global_error):
        self.global_error = global_error

    def download(self, url, bitrate):
        try:
            subprocess.check_output(f"{exe_path} download {url} --bitrate {bitrate} --output {download_path}", shell=True)
            return "Download Finished"
        except subprocess.CalledProcessError as e:
            print("Error: " + e.output)
            self.global_error.set_error(e.output)
            return e.output

def signal_handler(sig, frame):
    global download_thread
    global window_thread
    if download_thread and download_thread.is_alive():
        download_thread._stop()
    if window_thread and window_thread.is_alive():
        window_thread._stop()
    sys.exit(0)

def create_window():
    root = tk.Tk()
    root.title("SpotDL GUI")
    root.configure(bg="black")
    accent_color = "#00FF1F"
    downloading = False

    def path_select():
        global download_path 
        download_path = filedialog.askdirectory()
        
    def update_bitrate(*args):
        global current_bitrate
        position = int(bitrate_slider.get())
        bitreate_text.configure(text=f"Bitrate: {bitrates[position]}")
        current_bitrate = bitrates[position]
        root.after(100, update_bitrate)

    def download_button():
        global spotdl
        global error_handler
        global downloading
        global download_thread

        if not download_path:
            status.configure(text="No download path selected", fg="red")
            return
        if url_box.get() == "":
            status.configure(text="No URL entered", fg="red")
            return
        status.configure(text="Downloading...", fg="green")  
        # check if download thread is running
        if download_thread and download_thread.is_alive():
            status.configure(text="Already downloading", fg="red")
            return
        download_thread = threading.Thread(target=download)
        download_thread.daemon = True
        download_thread.start()


    def download():
        download_status = spotdl.download(url_box.get(), current_bitrate)    
        status.configure(text=download_status, fg="orange")
                

    def spacer():
        text = tk.Label(text=" ", fg=accent_color, bg="black")
        text.pack()

    image = tk.PhotoImage(file="spotify100.png", width=100, height=100)
    image_label = tk.Label(image=image, borderwidth=0)
    image_label.pack()

    info = tk.Label(text=f"SpotDL GUI\nby @petrouilfan\nv{SPOTDL_VERSION}", fg=accent_color, bg="black")
    info.pack()

    spacer()
    spacer()

    status = tk.Label(text="Status: Idle", fg=accent_color, bg="black")
    status.pack()

    spacer()

    _url = tk.Label(text="URL:", fg=accent_color, bg="black")
    _url.pack()
    url_box = tk.Entry(width=50, borderwidth=2, bg="black", fg=accent_color)
    url_box.pack()

    spacer()
    button = tk.Button(text="Download Path Select", fg="black", bg=accent_color, borderwidth=0, command=path_select)
    button.pack()

    spacer()
    bitreate_text = tk.Label(text=f"Bitrate: {bitrates[0]}", fg=accent_color, bg="black")
    bitreate_text.pack()
    bitrate_slider = tk.Scale(from_=0, to=3, orient=tk.HORIZONTAL, bg="black", fg=accent_color, highlightbackground="black", highlightcolor=accent_color, command=update_bitrate, showvalue=False)
    bitrate_slider.pack()
    


    spacer()
    button = tk.Button(text="Download", fg="black", bg=accent_color, borderwidth=0, command=download_button)
    button.pack()

    spacer()
    root.mainloop()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    global_error = ErrorHandler()
    spotdl = SpotDL(global_error)
    window_thread = threading.Thread(target=create_window)
    window_thread.daemon = True
    window_thread.start()
    while window_thread.is_alive():
        if global_error.error:
            print(global_error.error_message)
        time.sleep(1)