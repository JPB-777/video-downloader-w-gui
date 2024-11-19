"""
Video downloader GUI application.
"""
import os
import threading
import webbrowser
from datetime import datetime, timedelta
import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from tkinter import messagebox, filedialog, Text, END, StringVar

from ..core.platforms.youtube import YouTubeDownloader
from ..core.platforms.supported_sites import get_supported_sites, get_site_by_url, is_url_supported
from ..core.download_manager import DownloadManager
from ..core.download_types import DownloadTask, DownloadStatus
from .download_manager_frame import DownloadManagerFrame

class VideoDownloaderGUI:
    def __init__(self, master=None, theme='darkly'):
        # Initialize theme
        self.current_theme = theme
        print(f"Initial theme set to: {self.current_theme}")
        
        # Create root window
        self.master = master or tk.Tk()
        self.master.title("Advanced Video Downloader")
        self.master.geometry("1200x800")
        
        # Apply the theme
        self.style = Style(theme=self.current_theme)
        
        # Configure root window background based on theme
        self._configure_window_theme()

        # Initialize managers
        self.downloader = YouTubeDownloader()
        self.download_manager = DownloadManager()
        
        # Get supported sites
        self.supported_sites = get_supported_sites()

        # Setup UI components
        self._create_widgets()
        
        # Populate supported sites
        self._populate_supported_sites()

    def _configure_window_theme(self):
        """Configure window colors based on current theme."""
        if self.current_theme == 'darkly':
            bg_color = '#212529'  # Dark background
            fg_color = '#ffffff'  # Light text
        else:
            bg_color = '#ffffff'  # Light background
            fg_color = '#212529'  # Dark text
        
        # Configure the root window and all its children
        self.master.configure(bg=bg_color)
        for widget in self.master.winfo_children():
            try:
                widget.configure(bg=bg_color)
            except:
                pass
            
        # Configure ttk styles
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=fg_color)
        self.style.configure('TButton', background=bg_color)
        self.style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        self.style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
        self.style.configure('Treeview', background=bg_color, foreground=fg_color, fieldbackground=bg_color)

    def _create_widgets(self):
        # Main container with horizontal layout
        main_container = ttk.Frame(self.master)
        main_container.pack(fill=BOTH, expand=YES, padx=20, pady=20)

        # Theme toggle button in top right
        theme_frame = ttk.Frame(main_container)
        theme_frame.pack(fill=X, pady=(0, 10))
        
        # Initialize theme button - show Light Theme in dark mode, Dark Theme in light mode
        button_text = "☀️ Light Theme" if self.current_theme == 'darkly' else "🌙 Dark Theme"
        self.theme_btn = ttk.Button(
            theme_frame,
            text=button_text,
            command=self._toggle_theme,
            bootstyle=(SECONDARY, OUTLINE)
        )
        self.theme_btn.pack(side=RIGHT)

        # Left panel for supported sites (1/4 width)
        sites_frame = ttk.LabelFrame(main_container, text="Supported Platforms", padding=10)
        sites_frame.pack(side=LEFT, fill=BOTH, expand=NO, padx=(0, 10))

        # Create scrollable text widget for supported sites
        sites_scroll = ttk.Scrollbar(sites_frame)
        sites_scroll.pack(side=RIGHT, fill=Y)

        self.sites_text = Text(
            sites_frame,
            width=30,
            height=20,
            yscrollcommand=sites_scroll.set,
            wrap='word',
            state='disabled',
            cursor="hand2"  # Show hand cursor for clickable links
        )
        self.sites_text.pack(fill=BOTH, expand=YES)
        sites_scroll.config(command=self.sites_text.yview)

        # Configure text tags for styling
        self._configure_text_tags()

        # Bind click event for URLs
        self.sites_text.tag_bind("link", "<Button-1>", 
            lambda e: webbrowser.open(e.widget.get(f"@{e.x},{e.y} linestart", f"@{e.x},{e.y} lineend")))

        # Center panel for main content (2/4 width)
        content_frame = ttk.Frame(main_container)
        content_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)

        # Title
        title_label = ttk.Label(
            content_frame, 
            text="Video Downloader", 
            font=('-size', 16, '-weight', 'bold')
        )
        title_label.pack(pady=(0, 20))

        # URL Input
        url_frame = ttk.LabelFrame(content_frame, text="Video URLs (one per line)", padding=10)
        url_frame.pack(fill=X, pady=10)
        
        # Text widget for multiple URLs
        self.url_text = Text(url_frame, width=50, height=10)
        self.url_text.pack(fill=X, expand=YES)

        # Download Options Frame
        options_frame = ttk.LabelFrame(content_frame, text="Download Options", padding=10)
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
        path_frame = ttk.Frame(content_frame)
        path_frame.pack(fill=X, pady=10)
        
        ttk.Label(path_frame, text="Download Path:").pack(side=LEFT)
        self.path_entry = ttk.Entry(path_frame)
        self.path_entry.pack(side=LEFT, expand=YES, fill=X, padx=10)
        
        browse_btn = ttk.Button(
            path_frame, 
            text="Browse", 
            command=self._browse_directory,
            bootstyle=SUCCESS
        )
        browse_btn.pack(side=RIGHT)

        # Button Frame
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=10)

        # Download Button
        download_btn = ttk.Button(
            button_frame, 
            text="Download Now", 
            command=self._start_download,
            bootstyle=(PRIMARY, OUTLINE)
        )
        download_btn.pack(side=LEFT, padx=5)

        # Schedule Button
        schedule_btn = ttk.Button(
            button_frame,
            text="Schedule Download",
            command=self._schedule_download,
            bootstyle=(INFO, OUTLINE)
        )
        schedule_btn.pack(side=LEFT, padx=5)

        # Quit Button
        quit_btn = ttk.Button(
            button_frame,
            text="Quit",
            command=self.master.quit,
            bootstyle=(DANGER, OUTLINE)
        )
        quit_btn.pack(side=LEFT, padx=5)

        # Right panel for download manager (1/4 width)
        self.download_manager_frame = DownloadManagerFrame(main_container, self.download_manager)
        self.download_manager_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(10, 0))

    def _populate_supported_sites(self):
        """Populate the supported sites text widget."""
        self.sites_text.config(state='normal')
        self.sites_text.delete(1.0, END)
        
        for site in self.supported_sites:
            # Add site name
            self.sites_text.insert(END, f"{site.name}\n", "title")
            
            # Add clickable URL with proper protocol
            url = f"https://www.{site.base_url}"
            self.sites_text.insert(END, url, "link")
            self.sites_text.insert(END, "\n\n")  # Add spacing between sites
        
        self.sites_text.config(state='disabled')

    def _browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, directory)

    def _create_download_task(self, url: str, scheduled_time: datetime = None) -> DownloadTask:
        """Create a download task from the current UI state."""
        return DownloadTask(
            url=url,
            download_path=self.path_entry.get(),
            video_format=self.format_var.get(),
            resolution=self.resolution_var.get(),
            scheduled_time=scheduled_time,
            platform=get_site_by_url(url).name if get_site_by_url(url) else None
        )

    def _start_download(self):
        """Start downloading videos."""
        # Get URLs (split by newlines and remove empty lines)
        urls = [url.strip() for url in self.url_text.get("1.0", END).split('\n') if url.strip()]
        download_path = self.path_entry.get()

        # Input validation
        if not urls:
            messagebox.showerror("Error", "Please enter at least one URL.")
            return
        if not download_path:
            messagebox.showerror("Error", "Please select a download path.")
            return

        # Validate URLs
        unsupported_urls = [url for url in urls if not is_url_supported(url)]
        if unsupported_urls:
            messagebox.showerror(
                "Unsupported URLs", 
                "The following URLs are not from supported platforms:\n\n" +
                "\n".join(unsupported_urls)
            )
            return

        # Create and add download tasks
        for url in urls:
            task = self._create_download_task(url)
            self.download_manager.add_download(task)

        # Clear URL input
        self.url_text.delete(1.0, END)

    def _schedule_download(self):
        """Open a dialog to schedule the download."""
        # Create schedule dialog
        dialog = tk.Toplevel(self.master)
        dialog.title("Schedule Download")
        dialog.geometry("400x300")
        dialog.transient(self.master)  # Make dialog modal
        
        # Apply current theme's colors to dialog
        if self.current_theme == 'darkly':
            bg_color = '#212529'
            fg_color = '#ffffff'
        else:
            bg_color = '#ffffff'
            fg_color = '#212529'
            
        dialog.configure(bg=bg_color)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        # Create Delay tab
        delay_frame = ttk.Frame(notebook)
        notebook.add(delay_frame, text="Preset Delay")
        
        # Preset delay options
        delay_label = ttk.Label(delay_frame, text="Choose delay:", font=('Helvetica', 12))
        delay_label.pack(pady=10)
        
        delays = [
            ("30 minutes", 30),
            ("1 hour", 60),
            ("5 hours", 300),
            ("10 hours", 600)
        ]
        
        selected_delay = tk.StringVar(value="30")
        
        for text, minutes in delays:
            rb = ttk.Radiobutton(
                delay_frame, 
                text=text,
                value=str(minutes),
                variable=selected_delay
            )
            rb.pack(pady=5)
            
        # Create Specific Time tab
        time_frame = ttk.Frame(notebook)
        notebook.add(time_frame, text="Specific Time")
        
        time_label = ttk.Label(time_frame, text="Choose time:", font=('Helvetica', 12))
        time_label.pack(pady=10)
        
        # Time selection frame
        time_select_frame = ttk.Frame(time_frame)
        time_select_frame.pack(pady=10)
        
        # Hour selection (12-hour format)
        hour_var = tk.StringVar(value="12")
        hour_spinbox = ttk.Spinbox(
            time_select_frame,
            from_=1,
            to=12,
            width=3,
            textvariable=hour_var
        )
        hour_spinbox.pack(side=LEFT, padx=2)
        
        ttk.Label(time_select_frame, text=":").pack(side=LEFT)
        
        # Minute selection
        minute_var = tk.StringVar(value="00")
        minute_spinbox = ttk.Spinbox(
            time_select_frame,
            values=["00", "15", "30", "45"],  # Only allow quarter-hour increments
            width=3,
            textvariable=minute_var,
            state="readonly"  # Prevent manual entry to ensure valid values
        )
        minute_spinbox.pack(side=LEFT, padx=2)
        
        # AM/PM selection
        ampm_var = tk.StringVar(value="AM")
        ampm_combo = ttk.Combobox(
            time_select_frame,
            values=["AM", "PM"],
            textvariable=ampm_var,
            width=4,
            state="readonly"
        )
        ampm_combo.pack(side=LEFT, padx=5)
        
        def schedule():
            try:
                if notebook.index(notebook.select()) == 0:
                    # Delay tab selected
                    minutes = int(selected_delay.get())
                    delay_seconds = minutes * 60
                    self._start_scheduled_download(delay_seconds)
                else:
                    # Specific time tab selected
                    hour = int(hour_var.get())
                    minute = int(minute_var.get())
                    is_pm = ampm_var.get() == "PM"
                    
                    # Convert to 24-hour format
                    if is_pm and hour != 12:
                        hour += 12
                    elif not is_pm and hour == 12:
                        hour = 0
                    
                    # Calculate delay until specified time
                    now = datetime.now()
                    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                    # If target time is earlier than now, add a day
                    if target_time <= now:
                        target_time += timedelta(days=1)
                    
                    delay_seconds = int((target_time - now).total_seconds())
                    self._start_scheduled_download(delay_seconds)
                
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid time format: {str(e)}")
        
        # Create a frame for the button with proper background
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        # Schedule button with proper styling
        schedule_btn = ttk.Button(
            button_frame,
            text="Schedule Download",
            command=schedule,
            style="primary.TButton"  # Using primary style instead of Accent
        )
        schedule_btn.pack()
        
        # Center the dialog on the screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def _start_scheduled_download(self, delay_seconds):
        """Schedule downloads for later."""
        # Get URLs
        urls = [url.strip() for url in self.url_text.get("1.0", END).split('\n') if url.strip()]
        if not urls:
            messagebox.showerror("Error", "Please enter at least one URL.")
            return

        # Calculate scheduled time
        scheduled_time = datetime.now() + timedelta(seconds=delay_seconds)

        for url in urls:
            task = self._create_download_task(url, scheduled_time)
            self.download_manager.schedule_download(task, scheduled_time)

        # Clear URL input
        self.url_text.delete(1.0, END)
        messagebox.showinfo(
            "Downloads Scheduled",
            f"Downloads scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def _configure_text_tags(self):
        """Configure text tags based on current theme."""
        self.sites_text.tag_configure("title", font=("-size", 12, "-weight", "bold"))
        # Use different link colors for light/dark themes
        link_color = "#2962ff" if self.current_theme == 'cosmo' else "#00ffcc"  # Material Blue 700 for light theme
        self.sites_text.tag_configure("link", foreground=link_color, underline=True)

    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        try:
            # Print current theme before toggle
            print(f"Before toggle - Current theme: {self.current_theme}")
            
            # Toggle theme
            self.current_theme = 'cosmo' if self.current_theme == 'darkly' else 'darkly'
            print(f"After toggle - Current theme: {self.current_theme}")
            
            # Update the style theme
            try:
                self.style.theme_use(self.current_theme)
            except Exception as theme_error:
                print(f"Theme change error (non-critical): {theme_error}")
            
            # Configure window colors
            self._configure_window_theme()
            
            # Update button text - show Light Theme in dark mode, Dark Theme in light mode
            button_text = "☀️ Light Theme" if self.current_theme == 'darkly' else "🌙 Dark Theme"
            print(f"Setting button text to: {button_text}")
            self.theme_btn.configure(text=button_text)
            
            # Update link colors and refresh supported sites
            self._configure_text_tags()
            self._populate_supported_sites()
            
        except Exception as e:
            print(f"Theme toggle error: {e}")
            import traceback
            traceback.print_exc()

    def run(self):
        self.master.mainloop()
