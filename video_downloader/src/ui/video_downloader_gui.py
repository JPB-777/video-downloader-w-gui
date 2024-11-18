import os
import threading

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog

from ..core.platforms.youtube import YouTubeDownloader

class VideoDownloaderGUI:
    """
    Modern, bootstrap-styled Tkinter GUI for video downloading.
    """
    def __init__(self, master=None, theme='darkly'):
        """
        Initialize the GUI with a modern bootstrap theme.
        
        Args:
            master (ttk.Window, optional): Root window
            theme (str, optional): Bootstrap theme name
        """
        # Create root window with bootstrap styling
        self.master = master or ttk.Window(themename=theme)
        self.master.title("Advanced Video Downloader")
        self.master.geometry("600x600")

        # Initialize downloader
        self.downloader = YouTubeDownloader()

        # Setup UI components
        self._create_widgets()

    def _create_widgets(self):
        """
        Create modern, bootstrap-styled UI components.
        """
        # Container for all widgets
        container = ttk.Frame(self.master, padding=20)
        container.pack(fill=BOTH, expand=YES)

        # Title
        title_label = ttk.Label(
            container, 
            text="Video Downloader", 
            font=('-size', 16, '-weight', 'bold')
        )
        title_label.pack(pady=(0, 20))

        # URL Input
        url_frame = ttk.Frame(container)
        url_frame.pack(fill=X, pady=10)
        
        ttk.Label(url_frame, text="Video URL:").pack(side=LEFT)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side=LEFT, expand=YES, fill=X, padx=10)

        # Download Options Frame
        options_frame = ttk.LabelFrame(container, text="Download Options", padding=10)
        options_frame.pack(fill=X, pady=10)

        # Format Selection
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill=X, pady=5)
        ttk.Label(format_frame, text="Format:").pack(side=LEFT)
        self.format_var = ttk.StringVar(value="mp4")
        formats = ["mp4", "webm", "avi"]
        self.format_dropdown = ttk.Combobox(
            format_frame, 
            textvariable=self.format_var, 
            values=formats, 
            state="readonly",
            width=20
        )
        self.format_dropdown.pack(side=RIGHT)

        # Resolution Selection
        resolution_frame = ttk.Frame(options_frame)
        resolution_frame.pack(fill=X, pady=5)
        ttk.Label(resolution_frame, text="Resolution:").pack(side=LEFT)
        self.resolution_var = ttk.StringVar(value="720p")
        resolutions = ["360p", "480p", "720p", "1080p"]
        self.resolution_dropdown = ttk.Combobox(
            resolution_frame, 
            textvariable=self.resolution_var, 
            values=resolutions, 
            state="readonly",
            width=20
        )
        self.resolution_dropdown.pack(side=RIGHT)

        # Download Path
        path_frame = ttk.Frame(container)
        path_frame.pack(fill=X, pady=10)
        
        ttk.Label(path_frame, text="Download Path:").pack(side=LEFT)
        self.path_entry = ttk.Entry(path_frame, width=40)
        self.path_entry.pack(side=LEFT, expand=YES, fill=X, padx=10)
        
        browse_btn = ttk.Button(
            path_frame, 
            text="Browse", 
            command=self._browse_directory,
            bootstyle=SUCCESS
        )
        browse_btn.pack(side=RIGHT)

        # Progress Bar
        self.progress_var = ttk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            container, 
            variable=self.progress_var, 
            maximum=100, 
            length=500, 
            mode='determinate',
            bootstyle=SUCCESS
        )
        self.progress_bar.pack(pady=10)

        # Download Button
        download_btn = ttk.Button(
            container, 
            text="Download Video", 
            command=self._start_download,
            bootstyle=(PRIMARY, OUTLINE)
        )
        download_btn.pack(pady=10)

        # Status Display
        self.status_var = ttk.StringVar()
        status_label = ttk.Label(
            container, 
            textvariable=self.status_var, 
            wraplength=500,
            bootstyle=INFO
        )
        status_label.pack(pady=10)

    def _browse_directory(self):
        """
        Open a directory selection dialog and update download path.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, directory)

    def _start_download(self):
        """
        Validate inputs and start download in a separate thread.
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
        """
        def _update_ui():
            self.progress_var.set(100)
            self.status_var.set(f"Successfully downloaded: {title}")
            messagebox.showinfo("Success", f"Video '{title}' downloaded successfully!")
            
            # Clear input fields
            self.url_entry.delete(0, END)
        
        return _update_ui

    def run(self):
        """
        Start the Tkinter event loop.
        """
        self.master.mainloop()
