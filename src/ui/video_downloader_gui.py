import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

from ..core.platforms.youtube import YouTubeDownloader

class VideoDownloaderGUI:
    """
    Tkinter-based GUI for the video downloader application.
    Handles user interactions and delegates download tasks.
    """
    def __init__(self, master=None):
        """
        Initialize the GUI with a Tkinter root window.
        
        Args:
            master (tk.Tk, optional): Root window. Creates a new one if not provided.
        """
        # Create root window if not provided
        self.master = master or tk.Tk()
        self.master.title("Advanced Video Downloader")
        self.master.geometry("600x500")

        # Initialize downloader
        self.downloader = YouTubeDownloader()

        # Setup UI components
        self._create_widgets()

    def _create_widgets(self):
        """
        Create and layout all UI widgets for the application.
        Uses modern ttk widgets and grid/pack layout managers.
        """
        # URL Input Frame
        url_frame = ttk.Frame(self.master)
        url_frame.pack(padx=20, pady=10, fill='x')
        
        ttk.Label(url_frame, text="Video URL:").pack(side='left')
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side='left', expand=True, fill='x', padx=10)

        # Download Options Frame
        options_frame = ttk.LabelFrame(self.master, text="Download Options")
        options_frame.pack(padx=20, pady=10, fill='x')

        # Format Selection
        ttk.Label(options_frame, text="Format:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.format_var = tk.StringVar(value="mp4")
        formats = ["mp4", "webm", "avi"]
        self.format_dropdown = ttk.Combobox(
            options_frame, 
            textvariable=self.format_var, 
            values=formats, 
            state="readonly"
        )
        self.format_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Resolution Selection
        ttk.Label(options_frame, text="Resolution:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.resolution_var = tk.StringVar(value="720p")
        resolutions = ["360p", "480p", "720p", "1080p"]
        self.resolution_dropdown = ttk.Combobox(
            options_frame, 
            textvariable=self.resolution_var, 
            values=resolutions, 
            state="readonly"
        )
        self.resolution_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Download Path Frame
        path_frame = ttk.Frame(self.master)
        path_frame.pack(padx=20, pady=10, fill='x')
        
        ttk.Label(path_frame, text="Download Path:").pack(side='left')
        self.path_entry = ttk.Entry(path_frame, width=40)
        self.path_entry.pack(side='left', expand=True, fill='x', padx=10)
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self._browse_directory)
        browse_btn.pack(side='right')

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.master, 
            variable=self.progress_var, 
            maximum=100, 
            length=500, 
            mode='determinate'
        )
        self.progress_bar.pack(padx=20, pady=10)

        # Download Button
        download_btn = ttk.Button(
            self.master, 
            text="Download Video", 
            command=self._start_download
        )
        download_btn.pack(pady=10)

        # Status Display
        self.status_var = tk.StringVar()
        status_label = ttk.Label(
            self.master, 
            textvariable=self.status_var, 
            wraplength=500
        )
        status_label.pack(pady=10)

    def _browse_directory(self):
        """
        Open a directory selection dialog and update download path.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def _start_download(self):
        """
        Validate inputs and start download in a separate thread.
        Prevents UI from freezing during download.
        """
        # Gather input values
        url = self.url_entry.get()
        download_path = self.path_entry.get()
        video_format = self.format_var.get()
        resolution = self.resolution_var.get()

        # Input validation
        if not url or not download_path:
            messagebox.showerror("Error", "Please enter a URL and select a download path.")
            return

        # Reset progress bar
        self.progress_var.set(0)
        self.status_var.set("Preparing download...")

        # Use threading to prevent UI freezing
        download_thread = threading.Thread(
            target=self._download_video, 
            args=(url, download_path, video_format, resolution)
        )
        download_thread.start()

    def _download_video(self, url, download_path, video_format, resolution):
        """
        Perform video download using the core downloader.
        Handles UI updates and error messages.
        
        Args:
            url (str): Video URL
            download_path (str): Download directory
            video_format (str): Desired video format
            resolution (str): Desired video resolution
        """
        try:
            # Perform download
            downloaded_file = self.downloader.download(
                url, 
                download_path, 
                video_format, 
                resolution
            )
            
            # Update UI on successful download
            self.master.after(0, self._download_complete(os.path.basename(downloaded_file)))

        except Exception as e:
            # Handle and display download errors
            self.master.after(0, lambda: messagebox.showerror("Download Error", str(e)))

    def _download_complete(self, title):
        """
        Display download completion message and reset UI.
        
        Args:
            title (str): Title of the downloaded video
        """
        def _update_ui():
            self.progress_var.set(100)
            self.status_var.set(f"Successfully downloaded: {title}")
            messagebox.showinfo("Success", f"Video '{title}' downloaded successfully!")
            
            # Clear input fields
            self.url_entry.delete(0, tk.END)
        
        return _update_ui

    def run(self):
        """
        Start the Tkinter event loop.
        """
        self.master.mainloop()
