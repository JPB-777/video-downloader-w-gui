"""
Common types used across the download management system.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class DownloadStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SCHEDULED = "scheduled"

@dataclass
class DownloadTask:
    url: str
    download_path: str
    video_format: str
    resolution: str
    status: DownloadStatus = DownloadStatus.PENDING
    scheduled_time: Optional[datetime] = None
    retries: int = 0
    error_message: Optional[str] = None
    platform: Optional[str] = None
    max_retries: int = 3
