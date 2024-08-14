import tkinter as tk
from tkinter import filedialog, messagebox
import os
import ffmpeg
import threading

class VideoCompressorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Video Compressor")
        self.geometry("500x300")
        self.configure(bg="#2c3e50")
        
        # Create a title label
        self.title_label = tk.Label(self, text="Video Compressor", font=("Arial", 24, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.title_label.pack(pady=20)
        
        # Create a file selection button
        self.select_button = tk.Button(self, text="Select Video", font=("Arial", 14), bg="#2980b9", fg="#ecf0f1", command=self.open_file_manager)
        self.select_button.pack(pady=10)
        
        # Label to display selected file
        self.file_label = tk.Label(self, text="No file selected", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.file_label.pack(pady=10)
        
        # Create a compress button (initially hidden)
        self.compress_button = tk.Button(self, text="Compress Video", font=("Arial", 14), bg="#27ae60", fg="#ecf0f1", command=self.start_compression)
        
        # Label to display progress or messages
        self.progress_label = tk.Label(self, text="", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.progress_label.pack(pady=10)

        # Variable to store the selected file
        self.selected_file = None

    def open_file_manager(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi")])
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.show_compress_button()
        else:
            self.file_label.config(text="No file selected")

    def show_compress_button(self):
        # Show the compress button if it is not already visible
        if not self.compress_button.winfo_ismapped():
            self.compress_button.pack(pady=10)

    def start_compression(self):
        # Hide the compress button and show the progress label
        self.compress_button.pack_forget()
        self.progress_label.config(text="Compression in progress...")
        
        # Start the compression in a separate thread to keep the UI responsive
        threading.Thread(target=self.compress_video).start()

    def compress_video(self):
        if not self.selected_file:
            messagebox.showwarning("No file selected", "Please select a video file to compress.")
            return
        
        input_file = self.selected_file
        video_dir = os.path.dirname(input_file)
        output_dir = os.path.join(video_dir, "compressed_videos")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, f"compressed_{os.path.basename(input_file)}")
        
        try:
            (
                ffmpeg
                .input(input_file)
                .output(output_file, vcodec='libx264', crf=23, preset='fast')
                .run()
            )
            self.progress_label.config(text=f"Compression completed: {output_file}")
        except ffmpeg.Error as e:
            self.progress_label.config(text=f"Error compressing video: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    app = VideoCompressorApp()
    app.mainloop()
