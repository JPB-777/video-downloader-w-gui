import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('video_downloader.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the video downloader application.
    Initializes and runs the GUI with comprehensive error handling.
    """
    try:
        # Print Python path for debugging
        logger.debug(f"Python Path: {sys.path}")
        
        # Attempt to import required modules
        import ttkbootstrap
        logger.debug("ttkbootstrap imported successfully")
        
        # Try to get version using importlib.metadata
        try:
            import importlib.metadata
            version = importlib.metadata.version('ttkbootstrap')
            logger.debug(f"ttkbootstrap version: {version}")
        except (ImportError, ModuleNotFoundError):
            logger.debug("Could not determine ttkbootstrap version")
        
        # Import the GUI using an absolute import
        from video_downloader.src.ui.video_downloader_gui import VideoDownloaderGUI
        logger.info("VideoDownloaderGUI imported successfully")
        
        # Initialize and run the application
        logger.info("Initializing Video Downloader Application")
        app = VideoDownloaderGUI()
        app.run()
    
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Detailed import error information:")
        logger.error(f"Python executable: {sys.executable}")
        logger.error(f"Python version: {sys.version}")
        logger.error(f"Python path: {sys.path}")
        
        # Try to provide more context about the import failure
        import importlib
        for module in ['ttkbootstrap', 'video_downloader.src.ui.video_downloader_gui']:
            try:
                importlib.import_module(module)
            except ImportError as import_err:
                logger.error(f"Failed to import {module}: {import_err}")
        
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
