"""
Download Manager module for handling concurrent downloads and queuing.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os
import threading
from typing import Dict, List, Optional
import queue

from .download_types import DownloadStatus, DownloadTask
from .download_history import DownloadHistory

class DownloadManager:
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self.download_queue = queue.Queue()
        self.active_downloads: Dict[str, DownloadTask] = {}
        self.completed_downloads: List[DownloadTask] = []
        self.failed_downloads: List[DownloadTask] = []
        self.scheduled_downloads: List[DownloadTask] = []
        self._lock = threading.Lock()
        self.history = DownloadHistory()
        self._load_history()

    def schedule_download(self, task: DownloadTask, scheduled_time: datetime) -> None:
        """Schedule a download for a future time."""
        task.scheduled_time = scheduled_time
        task.status = DownloadStatus.SCHEDULED
        self.scheduled_downloads.append(task)
        self.history.add_download(task)
        self.history.update_status(task, DownloadStatus.SCHEDULED)

        # Calculate delay in seconds
        delay = (scheduled_time - datetime.now()).total_seconds()
        if delay > 0:
            timer = threading.Timer(delay, self.add_download, args=[task])
            timer.start()

    def add_download(self, task: DownloadTask) -> None:
        """Add a new download task to the queue."""
        with self._lock:
            self.history.add_download(task)
            if task.scheduled_time:
                self.scheduled_downloads.append(task)
            else:
                self.download_queue.put(task)
                self._process_queue()

    def _start_download(self, task: DownloadTask) -> None:
        """Start a download task."""
        with self._lock:
            task.status = DownloadStatus.IN_PROGRESS
            self.active_downloads[task.url] = task
            self.history.update_status(task, DownloadStatus.IN_PROGRESS)
            self.executor.submit(self._download_worker, task)

    def _download_worker(self, task: DownloadTask) -> None:
        """Worker function for handling downloads."""
        try:
            # TODO: Implement actual download logic using yt-dlp or pytube
            # For now, this is a placeholder
            pass

        except Exception as e:
            task.error_message = str(e)
            if task.retries < task.max_retries:
                task.retries += 1
                task.status = DownloadStatus.PENDING
                self.add_download(task)
            else:
                self._update_task_status(task, DownloadStatus.FAILED, error_message=str(e))
        else:
            self._update_task_status(task, DownloadStatus.COMPLETED)

        finally:
            self._process_queue()

    def retry_failed(self) -> None:
        """Retry all failed downloads."""
        with self._lock:
            failed = self.failed_downloads.copy()
            self.failed_downloads.clear()
            for task in failed:
                task.retries = 0
                task.status = DownloadStatus.PENDING
                self.add_download(task)

    def _process_queue(self) -> None:
        """Process the download queue."""
        with self._lock:
            while not self.download_queue.empty() and len(self.active_downloads) < self.max_concurrent:
                task = self.download_queue.get()
                self._start_download(task)

    def _update_task_status(self, task: DownloadTask, status: DownloadStatus, error_message: Optional[str] = None):
        """Update task status and persist to history."""
        with self._lock:
            task.status = status
            task.error_message = error_message
            self.history.update_status(task, status, error_message)
            
            if status == DownloadStatus.COMPLETED:
                if task in self.active_downloads.values():
                    del self.active_downloads[task.url]
                self.completed_downloads.append(task)
            elif status == DownloadStatus.FAILED:
                if task in self.active_downloads.values():
                    del self.active_downloads[task.url]
                self.failed_downloads.append(task)

    def _load_history(self):
        """Load recent downloads from history."""
        recent = self.history.get_recent_downloads(50)
        for download in recent:
            task = DownloadTask(
                url=download["url"],
                download_path=download["download_path"],
                video_format=download["video_format"],
                resolution=download["resolution"],
                status=DownloadStatus(download["status"]),
                scheduled_time=download.get("scheduled_time"),
                retries=download["retries"],
                error_message=download["error_message"],
                platform=download["platform"]
            )
            
            if task.status == DownloadStatus.COMPLETED:
                self.completed_downloads.append(task)
            elif task.status == DownloadStatus.FAILED:
                self.failed_downloads.append(task)
            elif task.status == DownloadStatus.SCHEDULED:
                self.scheduled_downloads.append(task)
