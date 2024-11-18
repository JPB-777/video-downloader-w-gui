import os
import logging
from abc import ABC, abstractmethod

class BaseVideoDownloader(ABC):
    """
    Abstract base class for video downloaders.
    Defines the interface for platform-specific video download implementations.
    """
    def __init__(self, download_path=None):
        """
        Initialize the base downloader.
        
        Args:
            download_path (str, optional): Default download directory. 
                                           If None, uses current working directory.
        """
        self.download_path = download_path or os.getcwd()
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s',
            filename='video_downloader.log'
        )
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def download(self, url, download_path=None, video_format='mp4', resolution='720p'):
        """
        Abstract method to download a video.
        
        Args:
            url (str): URL of the video to download
            download_path (str, optional): Directory to save the video
            video_format (str, optional): Desired video format
            resolution (str, optional): Desired video resolution
        
        Raises:
            ValueError: If download fails or parameters are invalid
        """
        pass

    def _validate_path(self, path):
        """
        Validate and create download path if it doesn't exist.
        
        Args:
            path (str): Path to validate
        
        Returns:
            str: Validated absolute path
        """
        # Use provided path or default to class's download path
        path = path or self.download_path
        
        # Expand and normalize path
        path = os.path.abspath(os.path.expanduser(path))
        
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        
        return path

    def _log_download_attempt(self, url):
        """
        Log the download attempt.
        
        Args:
            url (str): URL of the video being downloaded
        """
        self.logger.info(f"Attempting to download video from: {url}")

    def _log_download_success(self, title, path):
        """
        Log successful download.
        
        Args:
            title (str): Title of the downloaded video
            path (str): Path where video was saved
        """
        self.logger.info(f"Successfully downloaded: {title} to {path}")

    def _log_download_error(self, error):
        """
        Log download errors.
        
        Args:
            error (Exception): Error that occurred during download
        """
        self.logger.error(f"Download failed: {str(error)}")
