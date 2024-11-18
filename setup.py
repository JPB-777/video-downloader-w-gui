from setuptools import setup, find_packages

setup(
    name='video_downloader',
    version='0.1.0',
    packages=find_packages(),
    description='A modern video downloader application',
    author='Your Name',
    author_email='your.email@example.com',
    install_requires=[
        'pytube',
        'yt-dlp',
        'typing',
        'ttkbootstrap',
        'setuptools',
        'importlib-metadata',
    ],
    entry_points={
        'console_scripts': [
            'video-downloader=video_downloader.src.main:main',
        ],
    },
    python_requires='>=3.13',
)
