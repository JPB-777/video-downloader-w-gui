Build me a Python GUI application for downloading videos from multiple websites. The app should have the following features:

##Core Functionality:

Support downloading videos from sites like YouTube and others using libraries such as pytube and yt-dlp.
Allow users to choose video formats (e.g., MP4, WEBM) and resolutions (e.g., 720p, 1080p).
Enable users to select a custom save location for the downloaded files.

Enhanced Functionalities and Features
1. Max Concurrent Downloads
Purpose: Limit the number of simultaneous downloads to manage system resources.
Implementation:
Use Python's concurrent.futures.ThreadPoolExecutor or the asyncio library to handle multiple downloads concurrently.
Add a user-configurable setting in the UI to specify the maximum number of concurrent downloads.
Queue additional download tasks if the limit is reached.
UI Element: A dropdown or spinbox in the settings for selecting the number of concurrent downloads.
2. Scheduled Downloads
Purpose: Allow users to schedule downloads at a specific time.
Implementation:
Use Python's threading.Timer or the schedule library.
After a user inputs the desired time, calculate the delay (current time vs. scheduled time).
Start the download process automatically when the delay elapses.
UI Element:
Add a time picker or a simple dropdown for selecting hours and minutes.
Include a "Start Later" button that schedules the download.
Note: Provide visual feedback in the app for scheduled downloads (e.g., a list showing when each will start).
3. Fallback for Unavailable Formats and Resolutions
Purpose: Automatically choose a compatible format or resolution if the user’s preference isn’t available.
Implementation:
Fetch available formats and resolutions using yt-dlp or similar library.
Create a prioritized list of formats (e.g., MP4 > AVI > WEBM).
Similarly, prioritize resolutions (e.g., 1080p > 720p > 480p).
Use a fallback mechanism in the download logic:
If the preferred format/resolution isn’t available, revert to the next available option.
UI Feedback:
Notify the user of the fallback selection via a message box or status log.
Error Handling: If no valid format/resolution is available, display an error.
4. Handling Failed or Incomplete Downloads
Purpose: Ensure stability and minimize frustration caused by failed downloads.
Implementation:
Implement retry logic for failed downloads.
Save partial downloads to disk, and allow resuming them later (if the library supports it, e.g., yt-dlp).
Track download status in a database or file (e.g., SQLite or a simple JSON file) with states like Pending, In Progress, Completed, and Failed.
If a download fails after multiple retries, log the error and notify the user.
UI Feedback:
Display the download status (e.g., retry attempts) in the UI.
Include a "Retry Failed Downloads" button.


##User Interface:

Use Tkinter for the GUI, styled with modern themes (e.g., ttk or tkinter-ttk-bootstrap) for a clean, modern look.
Include fields for the video URL, format selection, resolution selection, and a "Download" button.
Display progress feedback, such as a progress bar, for ongoing downloads.

##Error Handling:

Handle common errors like unsupported sites, failed downloads, or connection issues gracefully.
Provide meaningful error messages to the user.


##Maintainability:

Ensure the app is modular and easy to update for adding new features or supporting additional sites in the future.
Use clear, well-documented code to aid in future modifications.
Platform:

The app should be compatible with both Windows and Mac OS.