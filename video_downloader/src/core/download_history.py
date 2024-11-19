"""
Download history management using SQLite database.
"""
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .download_manager import DownloadTask, DownloadStatus

class DownloadHistory:
    def __init__(self):
        # Create data directory in user's home directory
        self.data_dir = Path.home() / ".video_downloader"
        self.data_dir.mkdir(exist_ok=True)
        
        # Database file path
        self.db_path = self.data_dir / "download_history.db"
        
        # Initialize database
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create downloads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    platform TEXT,
                    download_path TEXT NOT NULL,
                    video_format TEXT NOT NULL,
                    resolution TEXT NOT NULL,
                    status TEXT NOT NULL,
                    scheduled_time TIMESTAMP,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    error_message TEXT,
                    retries INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()

    def add_download(self, task: DownloadTask) -> int:
        """Add a new download task to history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO downloads (
                    url, platform, download_path, video_format,
                    resolution, status, scheduled_time, start_time,
                    retries, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.url,
                task.platform,
                task.download_path,
                task.video_format,
                task.resolution,
                task.status.value,
                task.scheduled_time,
                datetime.now(),
                task.retries,
                task.error_message
            ))
            
            return cursor.lastrowid

    def update_status(self, task: DownloadTask, status: DownloadStatus,
                     error_message: Optional[str] = None):
        """Update the status of a download task."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            updates = {
                "status": status.value,
                "error_message": error_message
            }
            
            if status == DownloadStatus.COMPLETED:
                updates["end_time"] = datetime.now()
            
            set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
            values = list(updates.values())
            
            cursor.execute(f"""
                UPDATE downloads
                SET {set_clause}
                WHERE url = ? AND end_time IS NULL
            """, values + [task.url])

    def get_recent_downloads(self, limit: int = 50) -> List[dict]:
        """Get recent downloads with their status."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT *
                FROM downloads
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]

    def get_download_stats(self) -> dict:
        """Get download statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get counts by status
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM downloads
                GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # Get total download count
            cursor.execute("SELECT COUNT(*) FROM downloads")
            total_downloads = cursor.fetchone()[0]
            
            # Get today's downloads
            cursor.execute("""
                SELECT COUNT(*)
                FROM downloads
                WHERE DATE(created_at) = DATE('now')
            """)
            today_downloads = cursor.fetchone()[0]
            
            return {
                "total_downloads": total_downloads,
                "today_downloads": today_downloads,
                "status_counts": status_counts
            }

    def clear_history(self, days_old: int = 30):
        """Clear download history older than specified days."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM downloads
                WHERE created_at < datetime('now', ?)
            """, (f'-{days_old} days',))
            
            conn.commit()

    def get_task_history(self, task: DownloadTask) -> List[dict]:
        """Get history for a specific download task."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT *
                FROM downloads
                WHERE url = ?
                ORDER BY created_at DESC
            """, (task.url,))
            
            return [dict(row) for row in cursor.fetchall()]
