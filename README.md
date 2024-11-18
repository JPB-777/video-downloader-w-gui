# Video Downloader Application

## Overview
A modern, cross-platform video downloader application with a sleek, bootstrap-styled GUI.

## Features
- Download videos from multiple platforms
- Customizable download formats and resolutions
- Modern, responsive UI
- Error handling and logging

## Prerequisites
- Python 3.13
- Homebrew (recommended for macOS)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/video_downloader.git
cd video_downloader
```

2. Create a virtual environment:
```bash
python3.13 -m venv venv
source venv/bin/activate
```

3. Install the application:
```bash
pip install -e .
```

## Running the Application

### Option 1: Using the Run Script (Recommended)
```bash
./run_venv.sh
```

### Option 2: Manual Activation
```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python -m video_downloader.src.main

# Deactivate when done
deactivate
```

## Development

### Running Tests
```bash
python test_imports.py
```

### Logging
Application logs are saved to `video_downloader.log`

## Troubleshooting
- Ensure you're using Python 3.13
- Check `video_downloader.log` for detailed error messages
- Verify all dependencies are installed in the virtual environment

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

## License
[MIT](https://choosealicense.com/licenses/mit/)
