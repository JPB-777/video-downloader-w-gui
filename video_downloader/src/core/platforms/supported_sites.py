"""
Supported video platforms configuration.
This module manages the list of supported video platforms and their capabilities.
"""

class VideoSite:
    def __init__(self, name, base_url, description, supported_formats=None):
        self.name = name
        self.base_url = base_url
        self.description = description
        self.supported_formats = supported_formats or ["mp4", "webm"]

    def __str__(self):
        return f"{self.name} ({self.base_url})"

    def get_details(self):
        """Returns a formatted string with site details."""
        return (
            f"Platform: {self.name}\n"
            f"URL: {self.base_url}\n"
            f"Description: {self.description}\n"
            f"Supported Formats: {', '.join(self.supported_formats)}"
        )

# List of supported video platforms
SUPPORTED_SITES = [
    VideoSite(
        "YouTube",
        "youtube.com",
        "World's largest video sharing platform",
        ["mp4", "webm", "3gp"]
    ),
    VideoSite(
        "Vimeo",
        "vimeo.com",
        "High-quality creative video platform",
        ["mp4", "webm"]
    ),
    VideoSite(
        "Dailymotion",
        "dailymotion.com",
        "Popular video sharing platform",
        ["mp4"]
    ),
    VideoSite(
        "Twitch",
        "twitch.tv",
        "Live streaming and gaming content platform",
        ["mp4"]
    ),
    VideoSite(
        "Facebook Video",
        "facebook.com",
        "Social media video content",
        ["mp4"]
    )
]

def get_supported_sites():
    """Returns the list of supported video sites."""
    return SUPPORTED_SITES

def get_site_by_url(url):
    """
    Find a supported site that matches the given URL.
    Returns None if no match is found.
    """
    return next(
        (site for site in SUPPORTED_SITES if site.base_url in url.lower()),
        None
    )

def is_url_supported(url):
    """Check if a given URL is from a supported platform."""
    return any(site.base_url in url.lower() for site in SUPPORTED_SITES)
