# Advanced Video Downloader

## Overview
A modular, object-oriented Python GUI application for downloading videos from multiple websites.

## Project Structure
```
video_downloader/
│
├── src/
│   ├── core/
│   │   ├── downloader.py      # Base downloader abstract class
│   │   └── platforms/
│   │       ├── youtube.py     # YouTube-specific downloader
│   │
│   ├── ui/
│   │   └── video_downloader_gui.py  # Tkinter GUI
│   │
│   └── main.py                # Application entry point
│
├── requirements.txt
└── README.md
```

## Features
- Modular, extensible architecture
- Download videos from YouTube
- Select video format and resolution
- Modern, responsive GUI
- Robust error handling
- Logging support

## Prerequisites
- Python 3.7+
- pytube
- yt-dlp

## Installation
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application:
```bash
python -m src.main
```

1. Enter a video URL
2. Select download format and resolution
3. Choose a download path
4. Click "Download Video"

## Extensibility
- Easy to add new platform-specific downloaders
- Separate UI and core logic for maintainability

## Logging
Application logs are saved to `video_downloader.log`

## Future Improvements
- Support for more video platforms
- Advanced download settings
- Batch download functionality

## License
MIT License
