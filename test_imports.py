import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_imports():
    print("Python executable:", sys.executable)
    print("Python version:", sys.version)
    print("Python path:", sys.path)
    
    print("\nTesting imports:")
    
    try:
        import ttkbootstrap
        print("ttkbootstrap imported successfully")
        # Use importlib.metadata to get version
        try:
            import importlib.metadata
            version = importlib.metadata.version('ttkbootstrap')
            print(f"ttkbootstrap version: {version}")
        except (ImportError, ModuleNotFoundError):
            print("Could not determine ttkbootstrap version")
    except ImportError as e:
        print("Failed to import ttkbootstrap:", e)
    
    try:
        from video_downloader.src.ui.video_downloader_gui import VideoDownloaderGUI
        print("VideoDownloaderGUI imported successfully")
    except ImportError as e:
        print("Failed to import VideoDownloaderGUI:", e)

if __name__ == "__main__":
    test_imports()
