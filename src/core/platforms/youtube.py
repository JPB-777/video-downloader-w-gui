import os
from typing import Optional
from ..downloader import BaseVideoDownloader

try:
    from pytube import YouTube
    import yt_dlp
except ImportError:
    print("Please install pytube and yt-dlp")
    exit(1)

class YouTubeDownloader(BaseVideoDownloader):
    """
    Platform-specific downloader for YouTube videos.
    Supports multiple download strategies using pytube and yt-dlp.
    """
    def download(
        self, 
        url: str, 
        download_path: Optional[str] = None, 
        video_format: str = 'mp4', 
        resolution: str = '720p'
    ) -> str:
        """
        Download a YouTube video with specified parameters.
        
        Args:
            url (str): YouTube video URL
            download_path (str, optional): Directory to save the video
            video_format (str, optional): Desired video format
            resolution (str, optional): Desired video resolution
        
        Returns:
            str: Path to the downloaded video file
        
        Raises:
            ValueError: If download fails
        """
        # Validate and prepare download path
        download_path = self._validate_path(download_path)
        
        # Log download attempt
        self._log_download_attempt(url)
        
        try:
            # First, try pytube
            try:
                return self._download_with_pytube(
                    url, download_path, video_format, resolution
                )
            
            # Fallback to yt-dlp if pytube fails
            except Exception as pytube_error:
                self.logger.warning(f"Pytube download failed: {pytube_error}")
                return self._download_with_ytdlp(
                    url, download_path, video_format, resolution
                )
        
        except Exception as e:
            # Log and re-raise any download errors
            self._log_download_error(e)
            raise ValueError(f"Failed to download video: {str(e)}")

    def _download_with_pytube(
        self, 
        url: str, 
        download_path: str, 
        video_format: str, 
        resolution: str
    ) -> str:
        """
        Download video using pytube library.
        
        Args:
            url (str): YouTube video URL
            download_path (str): Directory to save the video
            video_format (str): Desired video format
            resolution (str): Desired video resolution
        
        Returns:
            str: Path to the downloaded video file
        """
        # Create YouTube object
        yt = YouTube(url)
        
        # Filter streams based on format and resolution
        video = yt.streams.filter(
            progressive=True, 
            file_extension=video_format, 
            resolution=resolution
        ).first()
        
        if not video:
            raise ValueError(f"No stream found matching format {video_format} and resolution {resolution}")
        
        # Download the video
        downloaded_file = video.download(output_path=download_path)
        
        # Log successful download
        self._log_download_success(yt.title, downloaded_file)
        
        return downloaded_file

    def _download_with_ytdlp(
        self, 
        url: str, 
        download_path: str, 
        video_format: str, 
        resolution: str
    ) -> str:
        """
        Download video using yt-dlp library as a fallback.
        
        Args:
            url (str): YouTube video URL
            download_path (str): Directory to save the video
            video_format (str): Desired video format
            resolution (str): Desired video resolution
        
        Returns:
            str: Path to the downloaded video file
        """
        # Configure yt-dlp options
        ydl_opts = {
            'format': f'bestvideo[height<={resolution[:-1]}]+bestaudio/best[height<={resolution[:-1]}]',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }
        
        # Download using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'Unknown')
            
            # Find the downloaded file
            downloaded_file = ydl.prepare_filename(info_dict)
        
        # Log successful download
        self._log_download_success(video_title, downloaded_file)
        
        return downloaded_file
