"""
Download manager frame for the video downloader GUI.
"""
import tkinter as tk
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Dialog

from ..core.download_manager import DownloadManager
from ..core.download_types import DownloadTask, DownloadStatus

class DownloadManagerFrame(ttk.LabelFrame):
    def __init__(self, master, download_manager: DownloadManager):
        super().__init__(
            master,
            text="Download Manager",
            padding=10
        )
        self.download_manager = download_manager
        self._create_widgets()
        self._setup_auto_refresh()

    def _create_widgets(self):
        # Settings section
        settings_frame = ttk.LabelFrame(self, text="Settings", padding=5)
        settings_frame.pack(fill=X, pady=(0, 10))

        # Concurrent downloads limit
        concurrent_frame = ttk.Frame(settings_frame)
        concurrent_frame.pack(fill=X, pady=5)
        ttk.Label(concurrent_frame, text="Max Concurrent Downloads:").pack(side=LEFT)
        self.concurrent_var = tk.StringVar(value=str(self.download_manager.max_concurrent))
        concurrent_spinbox = ttk.Spinbox(
            concurrent_frame,
            from_=1,
            to=10,
            width=5,
            textvariable=self.concurrent_var,
            command=self._update_concurrent_limit
        )
        concurrent_spinbox.pack(side=RIGHT)

        # Downloads list
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=BOTH, expand=YES)

        # Create notebook for different download states
        self.notebook = ttk.Notebook(list_frame)
        self.notebook.pack(fill=BOTH, expand=YES)

        # Create tab containers and scrolled frames
        # Active downloads tab
        active_container = ttk.Frame(self.notebook)
        self.active_frame = ScrolledFrame(active_container, autohide=True)
        self.active_frame.pack(fill=BOTH, expand=YES)
        self.notebook.add(active_container, text="Active")

        # Queued downloads tab
        queued_container = ttk.Frame(self.notebook)
        self.queued_frame = ScrolledFrame(queued_container, autohide=True)
        self.queued_frame.pack(fill=BOTH, expand=YES)
        self.notebook.add(queued_container, text="Queued")

        # Scheduled downloads tab
        scheduled_container = ttk.Frame(self.notebook)
        self.scheduled_frame = ScrolledFrame(scheduled_container, autohide=True)
        self.scheduled_frame.pack(fill=BOTH, expand=YES)
        self.notebook.add(scheduled_container, text="Scheduled")

        # Completed downloads tab
        completed_container = ttk.Frame(self.notebook)
        self.completed_frame = ScrolledFrame(completed_container, autohide=True)
        self.completed_frame.pack(fill=BOTH, expand=YES)
        self.notebook.add(completed_container, text="Completed")

        # Failed downloads tab
        failed_container = ttk.Frame(self.notebook)
        self.failed_frame = ScrolledFrame(failed_container, autohide=True)
        self.failed_frame.pack(fill=BOTH, expand=YES)
        self.notebook.add(failed_container, text="Failed")

        # Action buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=X, pady=10)

        # Retry failed button
        self.retry_btn = ttk.Button(
            button_frame,
            text="Retry Failed Downloads",
            command=self._retry_failed,
            bootstyle=(WARNING, OUTLINE)
        )
        self.retry_btn.pack(side=LEFT, padx=5)

    def _setup_auto_refresh(self):
        """Setup automatic refresh of download status."""
        self._refresh_status()
        self.after(1000, self._setup_auto_refresh)

    def _refresh_status(self):
        """Refresh all download status displays."""
        self._update_download_list(
            self.active_frame,
            self.download_manager.active_downloads.values(),
            show_progress=True
        )
        self._update_download_list(
            self.queued_frame,
            [task for task in self.download_manager.download_queue.queue],
            show_cancel=True
        )
        self._update_download_list(
            self.scheduled_frame,
            self.download_manager.scheduled_downloads,
            show_time=True
        )
        self._update_download_list(
            self.completed_frame,
            self.download_manager.completed_downloads[-50:],  # Show last 50
            show_time=True
        )
        self._update_download_list(
            self.failed_frame,
            self.download_manager.failed_downloads,
            show_error=True
        )

        # Update tab text with counts
        self.notebook.tab(0, text=f"Active ({len(self.download_manager.active_downloads)})")
        self.notebook.tab(1, text=f"Queued ({self.download_manager.download_queue.qsize()})")
        self.notebook.tab(2, text=f"Scheduled ({len(self.download_manager.scheduled_downloads)})")
        self.notebook.tab(3, text=f"Completed ({len(self.download_manager.completed_downloads)})")
        self.notebook.tab(4, text=f"Failed ({len(self.download_manager.failed_downloads)})")

    def _update_download_list(self, frame, tasks, show_progress=False, 
                            show_cancel=False, show_time=False, show_error=False):
        """Update a specific download list frame."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()

        # Add new task widgets
        for task in tasks:
            task_frame = ttk.Frame(frame)
            task_frame.pack(fill=X, pady=2, padx=5)

            # Basic info
            info_text = f"{task.platform or 'Unknown'}: {task.url}"
            if show_time and task.scheduled_time:
                info_text = f"{task.scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} - {info_text}"
            if show_error and task.error_message:
                info_text = f"{info_text}\nError: {task.error_message}"

            ttk.Label(
                task_frame,
                text=info_text,
                wraplength=400
            ).pack(side=LEFT, expand=YES, fill=X)

            # Progress bar for active downloads
            if show_progress:
                progress = ttk.Progressbar(
                    task_frame,
                    length=100,
                    mode='determinate',
                    bootstyle=SUCCESS
                )
                progress.pack(side=LEFT, padx=5)
                # TODO: Update progress value when implemented

            # Cancel button for queued downloads
            if show_cancel:
                ttk.Button(
                    task_frame,
                    text="Cancel",
                    command=lambda t=task: self._cancel_download(t),
                    bootstyle=(DANGER, OUTLINE)
                ).pack(side=RIGHT, padx=5)

    def _update_concurrent_limit(self):
        """Update the maximum concurrent downloads limit."""
        try:
            new_limit = int(self.concurrent_var.get())
            if 1 <= new_limit <= 10:
                self.download_manager.max_concurrent = new_limit
        except ValueError:
            self.concurrent_var.set(str(self.download_manager.max_concurrent))

    def _retry_failed(self):
        """Retry all failed downloads."""
        self.download_manager.retry_failed()

    def _cancel_download(self, task: DownloadTask):
        """Cancel a queued download."""
        # TODO: Implement download cancellation
        pass
